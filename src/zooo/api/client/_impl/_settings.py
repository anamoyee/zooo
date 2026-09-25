from __future__ import annotations

import typing as t

import httpx
import typing_extensions as te
from nya_result.direct import Result

from ._base import _BaseClient, httpcat_errors

if t.TYPE_CHECKING:
	from ...type import ProfileInfo
	from ...type.zoo import ThemeID


class _SettingsClientMixin(_BaseClient):
	class TargetSettingsTD(te.TypedDict, closed=True):
		profile_visibility: t.NotRequired[bool]
		cosmetics_visibility: t.NotRequired[bool]
		theme: t.NotRequired[ThemeID]

	@httpcat_errors
	async def change_settings(
		self,
		profile: ProfileInfo,
		*,
		send_empty_requests: bool = False,
		**kwargs: t.Unpack[TargetSettingsTD],
	) -> Result[t.Literal[b"cool and good"], httpx.HTTPStatusError]:
		"""Change the settings of a profile via the API (`/zoo/api/profileSettings/:pid` endpoint), If any issues arise, they will be stored as a HTTPStatusError in the error variant.

		Pass only the settings you want to change - other settings will remain unchanged.

		If no settings were passed (i.e. ask not to change any settings, but you invoked this method):
			- if `send_empty_requests` is `True`, a request will be sent to the API, if it's successful it means the cookie you used for this request will be valid for any subsequent non-empty settings requests or zoo extended permissions requests.
			- if `send_empty_requests` is `False`, a Result.new_ok(b"cool and good") will be returned no questions asked (No HTTP requests will be sent!).

		Args:
			profile: The profile to change the settings of.
			send_empty_requests: Whether to send a request to the API if no settings were passed. Defaults to `False`.
			**kwargs: The settings to change. Pass only the settings you want to change - other settings will remain unchanged. See `Client.TargetSettingsTD` for the available settings to change.

		Returns:
			A `Result` containing:
				- `[ok]` `b"cool and good"` if successful, or
				- `[err]` an `httpx.HTTPStatusError` if the HTTP request fails.
		"""
		self._raise_if_outside_context_manager()

		class Kwargs2(te.TypedDict, closed=True):
			publicProfile: t.NotRequired[bool]
			showCosmetics: t.NotRequired[bool]
			theme: t.NotRequired[str]

		def convert_kwargs_to_colons_format(kwargs: self.TargetSettingsTD) -> Kwargs2:
			new_kwargs = Kwargs2()

			if "profile_visibility" in kwargs:
				new_kwargs["publicProfile"] = kwargs["profile_visibility"]

			if "cosmetics_visibility" in kwargs:
				new_kwargs["showCosmetics"] = kwargs["cosmetics_visibility"]

			if "theme" in kwargs:
				new_kwargs["theme"] = kwargs["theme"].value

			return new_kwargs

		kwargs_converted = convert_kwargs_to_colons_format(kwargs)

		if not send_empty_requests and not kwargs_converted:
			return Result.new_ok(b"cool and good")

		async with self.limiter:
			resp = await self.httpx_client.post(
				f"profileSettings/{profile}",
				json=kwargs_converted,
			)

		try:
			resp.raise_for_status()
		except httpx.HTTPStatusError as e:
			return Result.new_err(e)

		resp_content = resp.read()
		assert resp_content == b"cool and good", f"Unexpected response content: {resp_content!r}"
		return Result.new_ok(resp_content)
