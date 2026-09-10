import pathlib as p
import sys
from collections import Counter
from typing import Any, Literal, Protocol

import rich
import rich.text
from rich.table import Table

from ... import api


class CallableWithName[**P, R](Protocol):
	__name__: str

	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...


class _RegistryType:
	"""A collection of f-funcs, so you dont have do to f_funcs.__globals__().items()->filter for '___f_', etc."""

	def __init__(self) -> None:
		self.lst: list[CallableWithName[..., Any]] = []

	def __call__[F: CallableWithName[..., Any]](self, f: F) -> F:
		self.lst.append(f)
		return f

	def get_dict(self) -> dict[str, CallableWithName[..., Any]]:
		return {f.__name__.removeprefix("___f_"): f for f in self.lst}


REGISTERED = _RegistryType()


@REGISTERED
def ___f_export_to_file(*zuhs: api.Zoo, file: p.Path):
	"""In case you forgot to pass the '-x ...' argument you can crudely rectify the situation, this function was made for exactly that.

	Usage: export_to_file(*zuhs, file=pathlib.Path('./zooo_export.pkl'))

	This produces the same format as the '-x' switch, but it is not recommended to use this, but rather the aformentioned commandline parameter next time, for ease of use.

	Args:
		*zuhs: all `api.Zoo` instances to export, as a variadic argument.
		file: (keyword only) The file to export the zuhs to, must be a pathlib.Path instance.

	Raises:
		TypeError: If the file argument is not a pathlib.Path instance.
		ValueError: If the file argument exists and is not a file (e.g. a directory).
	"""
	if not isinstance(file, p.Path):
		msg = f"file=... must be a pathlib.Path instance, got {type(file).__name__!r} instead."
		raise TypeError(msg)

	if file.exists() and not file.is_file():
		msg_0 = "`file` must either not exist or be a file to overwrite."
		raise ValueError(msg_0)

	api.type.pickle_to_file(file, zuhs)


@REGISTERED
def ___f_reset_displayhook() -> Literal["Done!"]:
	"""Remove the colored sys.displayhook (The repl result will no longer be colored from this point onwards.).

	Returns:
		"Done!", which displays in the repl as a confirmation it worked.
	"""
	sys.displayhook = sys.__displayhook__
	return "Done!"


@REGISTERED
def ___f_rank_colors(
	zuhs: list[api.Zoo],
	*,
	include_no_color: bool = True,
	max: int = 10,  # noqa: A002
):
	"""Show a leaderboard of zoo colors, which ones are the most used.

	Args:
		zuhs: The list of zuhs (api.Zoo) to operate on, may be a subset you filtered.
		include_no_color: Whether to include the "Use did not use a paintbrush item to select a color yet on this profile" represented by an italic None. Note that the row with "no color" does not count towards the rank column
		max: The max amount of rows to display, use -1 to display up to unlimited amount of rows. 10 by default.
	"""
	counts = Counter(z.color for z in zuhs)

	sorted_counts = sorted(
		counts.items(),
		key=lambda x: x[1],
		reverse=True,
	)

	if not include_no_color:
		sorted_counts = [tup for tup in sorted_counts if tup[0] is not None]

	table = Table("#", "amt", "color")

	i = 0
	true_i = 0

	for color, amount in sorted_counts:
		if i == max and max != -1:
			break

		if color is not None:
			i += 1
		true_i += 1

		table.add_row(
			str(i),
			str(amount),
			rich.text.Text(f"{color:06x}", style=f"b #{color:06x}") if color is not None else rich.text.Text("None", style="i"),
		)

	rich.print(table)

	if left_from_max := len(sorted_counts) - true_i:
		rich.print(f"[i]{left_from_max} rows were truncated, use max=-1 argument to specify no limit[/]")
