import asyncio
from collections.abc import Callable, Coroutine, Iterable
from dataclasses import dataclass, field
from functools import partial

import aiohttp
import pydantic as pd
import tcrutils.result
import tcrutils.void
from aiolimiter import AsyncLimiter
from tcrutils.console import c


def _remove_duplicates(l: Iterable):
	"""Remove duplicates while keeping order."""
	seen = set()
	result = []
	for item in l:
		if item not in seen:
			result.append(item)
			seen.add(item)
	return result


class ZooResult(tcrutils.result.Result[Zoo, errors.ZMSError]): ...


class ListedProfilesResult(tcrutils.result.Result[list[ListedProfile], errors.ZMSError]): ...


@dataclass(kw_only=True)
class Client:
	cookie: str | None = field(default=None)
	rate_limiter: AsyncLimiter = field(default_factory=lambda: AsyncLimiter(1, 2))
	session: aiohttp.ClientSession = field(default_factory=aiohttp.ClientSession)
	verbose: bool = False
	zoo_pre_hook: Callable[[AnnouncerState, str], Coroutine[None, None, None]] = default_zoo_pre_announcer
	profiles_pre_hook: Callable[[AnnouncerState, str], Coroutine[None, None, None]] = default_profiles_pre_announcer
	zoo_post_hook: Callable[[AnnouncerState, str], Coroutine[None, None, None]] = tcrutils.void.avoid
	profiles_post_hook: Callable[[AnnouncerState, str], Coroutine[None, None, None]] = tcrutils.void.avoid
	deplete_ratelimit_on_with_enter: bool = False

	async def __aenter__(self) -> "Client":
		if self.deplete_ratelimit_on_with_enter:
			await self.rate_limiter.acquire(self.rate_limiter.max_rate)
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
		await self.close()

	async def close(self) -> None:
		"""Close the underlying aiohttp async client session."""
		await self.session.close()

	async def _request(
		self,
		*,
		method: str = "GET",
		endpoint: str,
		pass_cookie_if_available: bool = True,
		headers: dict = None,
		params: dict = None,
		json: dict = None,
		no_resp_to_json: bool = False,
		raise_for_status: bool = True,
		_pre=None,
		_post=None,
		**kwargs,
	) -> dict | aiohttp.ClientResponse:
		"""Perform a single request to colon's API and return the JSON data.

		Raises:
		- zms.ZooError (if the API returns an error)
		- aiohttp error (if anything else goes wrong)
		"""
		url = API_URL / endpoint

		if headers is None:
			headers = {}

		if params is None:
			params = {}

		if pass_cookie_if_available and self.cookie is not None and "Cookie" not in headers:
			headers["Cookie"] = self.cookie

		async with self.rate_limiter:
			if _pre is not None:
				await _pre()
			try:
				async with self.session.request(method=method, url=url, headers=headers, params=params, **({} if json is None else {"json": json}), **kwargs) as resp:
					if resp.status == 500:
						data = await resp.json()

						raise errors.InternalError(raw_json=data, msg=data.get("message", ""))

					if await resp.text() == "No profiles!":
						err_data = {
							"name": "No profiles!",
							"msg": "It doesn't look like this user has any profiles. Oh well!",
							"type": "notFound",
							"invalid": True,
						}

						raise errors.ListedProfileNotFoundError(
							name=err_data["name"],
							msg=err_data["msg"],
							type=err_data["type"],
							raw_json=err_data,
						)

					if raise_for_status:
						resp.raise_for_status()

					if no_resp_to_json:
						return resp
					return await resp.json()
			finally:
				if _post is not None:
					await _post()

	async def fetch_zoo(
		self,
		profile: ProfileInfo,
		*,
		_console_json_on_validation_error: bool = False,
		_pre=None,
		_post=None,
	) -> ZooResult:
		"""Request a `Zoo` (profile) from the `/api/profile` endpoint in the Zoo API.

		All *zoo* errors are returned by default. Use `(await client.fetch_zoo()).is_err()` to determine if an error was returned.
		"""
		data = await self._request(endpoint=f"profile/{profile}", _pre=_pre, _post=_post)

		error = errors.error_from_data_if_any(data)

		if error is not None:
			return ZooResult.new_err(error)

		if _console_json_on_validation_error:
			try:
				pf = Zoo(**data)
			except pd.ValidationError:
				c(data)
				raise
		else:
			pf = Zoo(**data)

		return ZooResult.new_ok(pf)

	async def fetch_profiles(
		self,
		profile: UserInfo,
		*,
		_console_json_on_validation_error: bool = False,
		_pre=None,
		_post=None,
	) -> ListedProfilesResult:
		"""Request a list of `ListedProfiles` from the `/api/profiles` endpoint in the Zoo API.

		All *zoo* errors are returned by default. Use `(await client.fetch_profiles()).is_err()` to determine if an error or a valid list was returned.
		"""
		data_list = await self._request(endpoint=f"profiles/{profile}", _pre=_pre, _post=_post)

		error = errors.error_from_data_if_any(data_list)

		if error is not None:
			return ListedProfilesResult.new_err(error)

		lst = []

		for data in data_list:
			if _console_json_on_validation_error:
				try:
					pf = ListedProfile(**data)
				except pd.ValidationError:
					c(data)
					raise
			else:
				pf = ListedProfile(**data)
			lst.append(pf)

		return ListedProfilesResult.new_ok(lst)

	async def fetch_zoo_mass(self, *profiles: ProfileInfo, **kwargs) -> dict[str, ZooResult]:
		"""Request multiple `Zoo`s from the `/api/profile` endpoint in the Zoo API.

		Error handling works the same as `.fetch_zoo()` (all *zoo* errors are returned for you to raise or handle on your own).

		If client received a zoo_pre_hook or zoo_post_hook, it will be called before and/or after each request respectively.

		All duplicate ids are removed.
		"""
		match profiles:
			case ([*_],):
				raise TypeError("Unpack your IDs before passing them to `.fetch_zoo_mass()`, like this: `client.fetch_zoo_mass(*ids)`, do not pass a list of IDs.")
		profiles = [str(x) for x in profiles]
		profiles = _remove_duplicates(profiles)

		state = AnnouncerState(ii=len(profiles))

		async def fetch(id):
			try:
				return await self.fetch_zoo(
					id,
					**kwargs,
					_pre=partial(self.zoo_pre_hook, state, id),
					_post=partial(self.zoo_post_hook, state, id),
				)
			except errors.ZMSError as e:
				return ZooResult.new_err(e)

		tasks = [fetch(id) for id in profiles]
		results = await asyncio.gather(*tasks)
		return dict(zip(profiles, results, strict=True))

	async def fetch_profiles_mass(self, *profiles: UserInfo, **kwargs) -> dict[str, ListedProfilesResult]:
		"""Request multiple `ListedProfile`s from the `/api/profiles` endpoint in the Zoo API.

		Error handling works the same as `.fetch_profiles()` (all *zoo* errors are returned for you to raise or handle on your own).

		If client received a profiles_pre_hook or profiles_post_hook, it will be called before and/or after each request respectively.

		All duplicate ids are removed.
		"""
		match profiles:
			case ([*_],):
				raise TypeError("Unpack your IDs before passing them to `.fetch_profiles_mass()`, like this: `client.fetch_profiles_mass(*ids)`, do not pass a list of IDs.")
		profiles = [str(x) for x in profiles]
		profiles = _remove_duplicates(profiles)

		state = AnnouncerState(ii=len(profiles))

		async def fetch(id):
			try:
				return await self.fetch_profiles(
					id,
					**kwargs,
					_pre=partial(self.profiles_pre_hook, state, id),
					_post=partial(self.profiles_post_hook, state, id),
				)
			except errors.ZMSError as e:
				return ListedProfilesResult.new_err(e)

		tasks = [fetch(id) for id in profiles]
		results = await asyncio.gather(*tasks)
		return dict(zip(profiles, results, strict=True))
