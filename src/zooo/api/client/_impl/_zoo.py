from __future__ import annotations

import typing as t

import httpx
import pydantic as pd
from nya_result.direct import Result

from ... import error
from ...type import NPCProfileInfo, ProfileInfo, UserInfo, Zoo
from ._base import _BaseClient, httpcat_errors

if t.TYPE_CHECKING:
	from ...utils import Json


def _try_parse_into_zoo(json: Json) -> Result[Zoo, error.ZoooError | httpx.HTTPStatusError | pd.ValidationError]:
	try:
		zoo = Zoo(**json)  # ty: ignore[invalid-argument-type]
	except pd.ValidationError as e:
		return Result.new_err(e)

	return Result.new_ok(zoo)


class _ZooClientMixin(_BaseClient):
	@httpcat_errors
	async def fetch_zoo(
		self,
		profile: (
			NPCProfileInfo  #
			| ProfileInfo
			| UserInfo
			| int
		),
		/,
	) -> Result[Zoo, error.ZoooError | httpx.HTTPStatusError | pd.ValidationError]:
		"""Fetch the zoo data from the API (`/zoo/api/profile/:pid` endpoint), parse it as a `Zoo` object and return it wrapped in a `Result`, if any zoo-related errors, like parsing the response or http status code errors occur, include them as the error variant of said result, if any catastrophic or structural errors happen, raise them (e.g. improper usage of context managers, etc.).

		Returns:
			A `Result` containing:
				- `[ok]` the `Zoo` object if successful, or
				- `[err]` an `zooo.error.Error` if any zoo-related errors occur.
				- `[err]` an `httpx.HTTPStatusError` if the HTTP request fails.
				- `[err]` a `pydantic.ValidationError` if the response cannot be parsed as a `Zoo` object.

		Raises:
			RuntimeError: if the client is not entered (i.e. not used in an async context manager).
		"""  # ruff: ignore[docstring-extraneous-exception]

		self._raise_if_outside_context_manager()

		async with self.limiter:
			resp = await self.httpx_client.get(f"profile/{profile}")

		try:
			resp.raise_for_status()
		except httpx.HTTPStatusError as e:
			return Result.new_err(e)

		json: Json = resp.json()

		if not isinstance(json, dict):
			return Result.new_err(error.MalformedJsonResponseError(raw_json=json))

		return _try_parse_into_zoo(json)
