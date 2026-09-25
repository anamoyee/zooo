import typing as t


class AsyncFn0[R](t.Protocol):
	async def __call__(self) -> R: ...

	__name__: str
