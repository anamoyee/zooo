import asyncio
from collections.abc import Callable
from dataclasses import dataclass, field

import aiohttp
import rich
from tcrutils.result import Result2 as Result
from tcrutils.result import aresultify2 as aresultify

from .. import error
from ..type import NPCProfileInfo, ProfileInfo, UserInfo, Zoo
from ._base import BaseClient, BaseHook, ResultDict


class ZooHook(BaseHook[UserInfo | ProfileInfo | NPCProfileInfo, Zoo]):
	async def post_ok(self, key: ProfileInfo, zuh: Zoo) -> None:
		rich.print(f"{self.make_counter()} [b][yellow]Fetched the profile [white]{key}[yellow].")
		pass

	async def post_err(self, key: UserInfo | ProfileInfo | NPCProfileInfo, err: Exception) -> None:
		await super().post_err(key, err)
		rich.print(f"{self.make_counter()} [b][red]Failed to fetch profile [white]{key}[red] due to {err.__class__.__name__!r}! Skipping... (consider removing this source from your ids file)")


@dataclass(kw_only=True)
class ZooClient(BaseClient):
	zoo_hook_factory: Callable[[], ZooHook] = field(default=ZooHook)

	async def _request_zoo(
		self,
		user: UserInfo | ProfileInfo,
	) -> tuple[aiohttp.ClientResponse, str, Result[dict, error.ZooError | Exception]]:
		"""Perform a single request to colon's API and return the JSON data.

		Raises:
		- zooo.error.ZooError (if the API returns an error)
		- aiohttp error (if anything else goes wrong)
		"""
		url = f"{self.base_url}/profile/{user}"

		headers = {}

		if self.cookie is not None and "Cookie" not in headers:
			headers["Cookie"] = self.cookie

		async with self.rate_limiter:
			async with self.session.get(url=url, headers=headers) as resp:
				if resp.status == 500:
					data = await resp.json()

					raise error.InternalError(raw_json=data, msg=data.get("message", ""))

				text = await resp.text()

				try:
					data = Result.new_ok(await resp.json())
				except Exception as e:
					data = Result.new_err(e)

				return resp, text, data

	@aresultify
	async def fetch_zoo(self, user: UserInfo | ProfileInfo | NPCProfileInfo | int) -> Zoo:
		if isinstance(user, int):
			user = UserInfo(user)

		_, _, data = await self._request_zoo(user)

		data.raise_if_possible()

		data = data.unwrap()

		error.raise_from_data(data)

		return Zoo(**data)

	async def fetch_zoo_mass(self, *users: UserInfo | ProfileInfo | int) -> ResultDict[UserInfo | ProfileInfo | NPCProfileInfo, Zoo, Exception]:
		users: set[UserInfo | ProfileInfo | NPCProfileInfo] = {(UserInfo(user) if isinstance(user, int) else user) for user in users}

		hook = self.zoo_hook_factory(users)

		async def task(user: UserInfo | ProfileInfo | NPCProfileInfo):
			await hook._pre_submit(user)

			zoo_result = await self.fetch_zoo(user)

			if zoo_result.is_ok:
				user = zoo_result.unwrap().id

			await hook._post_submit(user, zoo_result)

			return (user, zoo_result)

		tasks = (task(user) for user in users)

		return ResultDict(await asyncio.gather(*tasks))
