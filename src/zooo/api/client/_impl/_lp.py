from __future__ import annotations

import typing as t
from collections.abc import Collection

import httpx
import pydantic as pd
from nya_result.direct import Result

from ... import error
from ...type import ListedProfile, ProfileInfo, UserInfo
from ._base import _BaseClient, httpcat_errors

if t.TYPE_CHECKING:
	from ...utils import Json


def _try_parse_into_listed_profile(json: Json) -> Result[ListedProfile, pd.ValidationError]:
	try:
		listed_profile = ListedProfile(**json)  # ty: ignore[invalid-argument-type]
	except pd.ValidationError as e:
		return Result.new_err(e)

	return Result.new_ok(listed_profile)


class _LPClientMixin(_BaseClient):
	@httpcat_errors
	async def fetch_listed_profiles(
		self,
		profile: (
			ProfileInfo  #
			| UserInfo
			| int
		),
		/,
	) -> Result[Collection[ListedProfile], error.ZoooError | httpx.HTTPStatusError | error.ListedProfileValidationErrorGroup]:
		"""Fetch the listed profile data from the API (`/zoo/api/profiles/:uid` endpoint), parse it as a collection of `ListedProfile` objects and return it wrapped in a `Result`, if any zoo-related errors, like parsing the response or http status code errors occur, include them as the error variant of said result, if any catastrophic or structural errors happen, raise them (e.g. improper usage of context managers, etc.).

		Returns:
			A `Result` containing:
				- `[ok]` a collection of `ListedProfile` objects if successful, or
				- `[err]` an `zooo.error.Error` if any zoo-related errors occur.
				- `[err]` an `httpx.HTTPStatusError` if the HTTP request fails.
				- `[err]` a `zooo.error.ListedProfileValidationErrorGroup`, a group of `pydantic.ValidationError`s if any of the JSON fragments of the root JSON list cannot be parsed as `ListedProfile` objects.

		Raises:
			RuntimeError: if the client is not entered (i.e. not used in an async context manager).
		"""  # ruff: ignore[docstring-extraneous-exception]

		self._raise_if_outside_context_manager()

		async with self.limiter:
			resp = await self.httpx_client.get(f"profiles/{profile}")

		try:
			resp.raise_for_status()
		except httpx.HTTPStatusError as e:
			return Result.new_err(e)

		json: Json = resp.json()

		if not isinstance(json, list):
			return Result.new_err(error.MalformedJsonResponseError(raw_json=json))

		lp_results = [_try_parse_into_listed_profile(item) for item in json]

		if any(res.is_err for res in lp_results):
			return Result.new_err(
				error.ListedProfileValidationErrorGroup(
					"One or more listed profiles failed to validate against the ListedProfile model.",
					[res.unwrap_err() for res in lp_results if res.is_err],
				)
			)

		listed_profiles = tuple(res.unwrap() for res in lp_results if res.is_ok)

		return Result.new_ok(listed_profiles)
