import cProfile
import io
import os
import pstats
import sys
from collections.abc import Awaitable, Callable, Generator
from contextlib import contextmanager
from functools import wraps

MAX_LINES = 50


def _profiling_enabled() -> bool:
	return os.environ.get("PROFILING", "0").lower() in {"1", "true", "yes", "on"}


def profile[**P, R](f: Callable[P, R]) -> Callable[P, R]:
	"""Wrap the given function in a profiler (powered by `cProfile` and `pstats`), after the function exits print the result."""

	if not _profiling_enabled():
		return f

	profiled = _force_profile_returning(f)

	@wraps(f)
	def awrapper(*args: P.args, **kwargs: P.kwargs) -> R:
		(_, report_str), retval = profiled(*args, **kwargs)

		print(report_str, file=sys.stderr)

		return retval

	return awrapper


def _force_profile_returning[**P, R](f: Callable[P, R]) -> Callable[P, tuple[tuple[pstats.Stats, str], R]]:
	"""Wrap the given function in a profiler (powered by `cProfile` and `pstats`), after the function exits return a `2-tuple of (2-tuple of (pstats.Stats, formatted_pstats_report: str), R)`."""

	@wraps(f)
	def awrapper(*args: P.args, **kwargs: P.kwargs) -> tuple[tuple[pstats.Stats, str], R]:
		pr = cProfile.Profile()

		pr.enable()
		retval = f(*args, **kwargs)
		pr.disable()

		s = io.StringIO()
		sortby = "cumulative"
		stats = pstats.Stats(pr, stream=s).sort_stats(sortby)
		stats.print_stats(MAX_LINES)

		return (stats, s.getvalue()), retval

	return awrapper


def aprofile[**P, R](f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
	"""Wrap the given coroutine function in a profiler (powered by `cProfile` and `pstats`), after the function exits print the result."""

	if not _profiling_enabled():
		return f

	profiled = _force_aprofile_returning(f)

	@wraps(f)
	async def awrapper(*args: P.args, **kwargs: P.kwargs) -> R:
		(_, report_str), retval = await profiled(*args, **kwargs)

		print(report_str, file=sys.stderr)

		return retval

	return awrapper


def _force_aprofile_returning[**P, R](f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[tuple[tuple[pstats.Stats, str], R]]]:
	"""Wrap the given coroutine function in a profiler (powered by `cProfile` and `pstats`), after the function exits return a `2-tuple of (2-tuple of (pstats.Stats, formatted_pstats_report: str), R)`."""

	@wraps(f)
	async def awrapper(*args: P.args, **kwargs: P.kwargs) -> tuple[tuple[pstats.Stats, str], R]:
		pr = cProfile.Profile()

		pr.enable()
		retval = await f(*args, **kwargs)
		pr.disable()

		s = io.StringIO()
		sortby = "cumulative"
		stats = pstats.Stats(pr, stream=s).sort_stats(sortby)
		stats.print_stats(MAX_LINES)

		return (stats, s.getvalue()), retval

	return awrapper


@contextmanager
def contextmanager_profiling() -> Generator[None]:
	"""A context manager that profiles the code within its context (powered by `cProfile` and `pstats`), after the context exits print the result."""

	if not _profiling_enabled():
		yield
		return

	pr = cProfile.Profile()

	pr.enable()
	try:
		yield
	finally:
		pr.disable()

	s = io.StringIO()
	sortby = "cumulative"
	stats = pstats.Stats(pr, stream=s).sort_stats(sortby)
	stats.print_stats(MAX_LINES)

	print(s.getvalue(), file=sys.stderr)
