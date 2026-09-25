import dataclasses as dc
import datetime as dt
import functools
import typing as t
from collections.abc import Awaitable, Callable

import httpx
import httpx_limiter
import httpx_limiter.aiolimiter
from nya_result.direct import Result


def httpcat_errors[**P, R, E: Exception](
	f: Callable[P, Awaitable[Result[R, E]]], *, _url: str = "https://http.cat"
) -> Callable[P, Awaitable[Result[R, E]]]:
	"""Decorate a function returning nya_result.Result[..., httpx.HTTPStatusError], if result.is_err and isinstance(e, httpx.HTTPStatusError), replace the error's message to contain a link to http.cat instead of developer.mozzila.org/.../HTTP/Status/ and re-raise it."""

	def replace_on_arg(arg: object) -> str | object:
		if isinstance(arg, str):
			arg = arg.replace("https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/", f"{_url}/")

		return arg

	@functools.wraps(f)
	async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, E]:
		result = await f(*args, **kwargs)

		if result.is_ok:
			return result

		e = result.unwrap_err()

		if isinstance(e, httpx.HTTPStatusError):
			e.args = tuple(replace_on_arg(arg) for arg in e.args)

		return result

	return wrapper


@dc.dataclass(kw_only=True)
class _BaseClient:
	httpx_client: httpx.AsyncClient = dc.field(kw_only=False)
	limiter: httpx_limiter.aiolimiter.AiolimiterAsyncLimiter = dc.field(default_factory=lambda: _BaseClient.make_httpx_limiter())  # ruff: ignore[unnecessary-lambda]

	@staticmethod
	def make_httpx_client(
		cookie: str | None = None,
		*,
		_base_url: str = "https://gdcolon.com/zoo/api",
	) -> httpx.AsyncClient:
		"""Helper function to produce a `httpx.AsyncClient` configured for interacting with Zoo API.

		Args:
			cookie: Some methods may require a cookie to work, and some may provide extra functionality if one is provided (e.g. resolving descriptions which are normally hidden, resolving a profile if it's set to private).
			_base_url: The base URL for the Zoo API. Change only if you have your own Zoo API server. By default points to the official Zoo API server at `https://gdcolon.com/zoo/api`.

		Returns:
			A `httpx.AsyncClient` instance configured for interacting with Zoo API.
		"""

		httpx_client = httpx.AsyncClient(
			base_url=_base_url,
		)

		if cookie is not None:
			httpx_client.cookies.set("zoo", cookie.removeprefix("zoo="))

		return httpx_client

	@staticmethod
	def make_httpx_limiter(requests_per_second: int = 1) -> httpx_limiter.aiolimiter.AiolimiterAsyncLimiter:
		"""A shorthand for the incredibly verbose `httpx-limiter[aiolimiter]`'s syntax for creating a rate limiter. If you need further control than {int}/sec, use the verbose syntax directly."""
		return httpx_limiter.aiolimiter.AiolimiterAsyncLimiter.create(
			httpx_limiter.Rate(
				magnitude=requests_per_second,
				duration=dt.timedelta(seconds=1),
			)
		)

	def _raise_if_outside_context_manager(self) -> None:
		if self.httpx_client._state == httpx._client.ClientState.UNOPENED:
			msg_0 = 'Cannot use functional methods before entering the client context. Use "async with" to enter the client context first.'
			raise RuntimeError(msg_0)

		if self.httpx_client._state == httpx._client.ClientState.CLOSED:
			msg_1 = 'Cannot use functional methods after having exited the client context (left the "async with" block).'
			raise RuntimeError(msg_1)

	async def __aenter__(self) -> t.Self:
		await self.httpx_client.__aenter__()  # let the httpx client handle the error message if opened already

		return self

	async def __aexit__(self, _0, _1, _2) -> None:
		return await self.httpx_client.__aexit__(_0, _1, _2)
