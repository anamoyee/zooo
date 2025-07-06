import asyncio
import functools
from collections.abc import Generator, Sequence
from dataclasses import dataclass, field
from typing import Self

import aiohttp
from aiolimiter import AsyncLimiter
from pydantic import ValidationError
from tcrutils.console import c
from tcrutils.result import Result2 as Result


@dataclass(kw_only=True)
class BaseClient:
	cookie: str | None = field(default=None)
	rate_limiter: AsyncLimiter = field(default_factory=lambda: AsyncLimiter(1, 1))
	session: aiohttp.ClientSession = field(default_factory=aiohttp.ClientSession)
	base_url: str = field(default="https://gdcolon.com/zoo/api")

	async def __aenter__(self) -> Self:
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
		await self.close()

	async def close(self) -> None:
		"""Close the underlying aiohttp async client session."""
		await self.session.close()


class BaseHook[K, T]:
	@classmethod
	def _lock_wrapper(cls, method_name: str):
		orig_method = getattr(cls, method_name, None)
		if not orig_method:
			return cls

		@functools.wraps(orig_method)
		async def wrapped(self, *args, **kwargs):
			async with self.lock:
				return await orig_method(self, *args, **kwargs)

		setattr(cls, method_name, wrapped)
		return cls

	alock: asyncio.Lock
	keys: Sequence[K]

	@property
	def ii(self) -> int:
		return len(self.keys)

	i: int

	def __init__(self, keys: Sequence[K]) -> None:
		self.alock = asyncio.Lock()
		self.keys = keys
		self.i = 0

	async def _pre_submit(self, key: K):
		async with self.alock:
			await self.pre(key)

	async def _post_submit(self, key: K, result: Result[T, Exception]) -> None:
		async with self.alock:
			self.i += 1

			await self.post(key, result)

			if result.is_ok:
				await self.post_ok(key, result.unwrap())
			else:
				await self.post_err(key, result.unwrap_err())

	def make_counter(self) -> str:
		width = len(str(self.ii))

		return f"[b][black]{'[dim]0[/dim]' * (width - len(str(self.i)))}{self.i}[white]/[/][black]{self.ii}[/][/b]"

	async def pre(self, key: K, /) -> None:
		"""Called before every request."""

	async def post(self, key: K, result: Result[T, Exception], /) -> None:
		"""Called after every request before the object is constructed."""

	async def post_ok(self, key: K, value: T, /) -> None:
		"""Called after every successful request."""

	async def post_err(self, key: K, err: Exception, /) -> None:
		"""Called after every failed request. By default raise any pydantic.ValidationErrors. Do not super().post_Err() if you dont want this behaviour."""

		if isinstance(err, ValidationError):
			if hasattr(err, "raw_json"):
				c(err.raw_json)

			raise err


class ResultDict[K, V, E](dict[K, Result[V, E]]):
	def ok_values(self) -> Generator[V]:
		return (r.unwrap() for r in self.values() if r.is_ok)
