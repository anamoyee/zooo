import asyncio
from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass, field

import aiohttp
import rich
from tcrutils.console import c
from tcrutils.result import Result2 as Result
from tcrutils.result import aresultify2 as aresultify

from .. import error
from ..type import ListedProfile, UserInfo
from ._base import BaseClient, BaseHook, ResultDict


class ResultListDict[K, V, E](ResultDict[K, list[V], E]):
	def ok_values(self) -> Generator[V, None, None]:
		for lst in super().ok_values():
			yield from lst


class ListedProfilesHook(BaseHook[UserInfo, list[ListedProfile]]):
	async def post_ok(self, key: UserInfo, lps: list[ListedProfile]) -> None:
		rich.print(f"{self.make_counter()} [b][yellow]Fetched [white]{len(lps)} [yellow]profiles of [white]{key}[yellow].")
		pass

	async def post_err(self, key: UserInfo, err: Exception) -> None:
		await super().post_err(key, err)
		rich.print(f"{self.make_counter()} [b][red]Failed to fetch profiles of [white]{key}[red] due to {err.__class__.__name__!r}! Skipping...")


@dataclass(kw_only=True)
class ListedProfilesClient(BaseClient):
	listed_profile_hook_factory: Callable[[], ListedProfilesHook] = field(default=ListedProfilesHook)

	async def _request_listed_profile(
		self,
		user: UserInfo,
	) -> tuple[aiohttp.ClientResponse, str, Result[list, error.ListedProfileError | Exception]]:
		"""Perform a single request to colon's API and return the JSON data.

		Raises:
		- zooo.error.Error (if the API returns an error)
		- aiohttp error (if anything else goes wrong)
		"""
		url = f"{self.base_url}/profiles/{user}"

		headers = {}

		if self.cookie is not None and "Cookie" not in headers:
			headers["Cookie"] = self.cookie

		async with self.rate_limiter:
			async with self.session.get(url=url, headers=headers) as resp:
				if resp.status == 500:
					data = await resp.json()

					raise error.InternalError(raw_json=data, msg=data.get("message", ""))

				resp.raise_for_status()

				text = await resp.text()

				try:
					data = Result.new_ok(await resp.json())
				except Exception as e:
					data = Result.new_err(e)

				return resp, text, data

	@aresultify
	async def fetch_profiles(self, user: UserInfo | int) -> list[ListedProfile]:
		if isinstance(user, int):
			user = UserInfo(user)

		_, text, data = await self._request_listed_profile(user)

		if text == "No profiles!":
			err_data = {
				"name": "No profiles!",
				"msg": "It doesn't look like this user has any profiles. Oh well!",
				"type": "notFound",
				"invalid": True,
			}

			raise error.ListedProfileNotFoundError(
				name=err_data["name"],
				msg=err_data["msg"],
				type=err_data["type"],
				raw_json=err_data,
			)

		data.raise_if_possible()

		data = data.unwrap()

		error.raise_from_data(data)

		return [ListedProfile(**x) for x in data]

	async def fetch_profiles_mass(self, *users: UserInfo | int) -> ResultListDict[UserInfo, ListedProfile, Exception]:
		users: set[UserInfo] = {(UserInfo(user) if isinstance(user, int) else user) for user in users}

		hook = self.listed_profile_hook_factory(users)

		async def task(user: UserInfo):
			await hook._pre_submit(user)

			result = await self.fetch_profiles(user)

			await hook._post_submit(user, result)

			return (user, result)

		tasks = (task(user) for user in users)

		return ResultListDict(await asyncio.gather(*tasks))
