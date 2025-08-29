import builtins
import code
import pathlib
import pathlib as p
import sys
from collections import Counter

import rich
import rich.table
import rich.text
from rich.table import Table
from tcrutils.console import c
from tcrutils.decorator import instance
from tcrutils.print import FMTC, fmt_iterable

from ... import api

if True:  # f-funcs

	def ___f_export_to_file(*, file: p.Path):
		"""In case you forgot to pass the '-x ...' argument you can crudely rectify the situation.

		Usage: export_to_file(file=pathlib.Path('./zooo_export.pkl'))

		This produces the same format as the '-x' switch, but it is not recommended to use this, but rather the aformentioned commandline parameter next time.
		"""
		if not isinstance(file, p.Path):
			raise TypeError(f"file=... must be a pathlib.Path instance, got {type(file).__name__!r} instead.")

		if file.exists() and not file.is_file():
			raise ValueError("'file' must either not exist or be a file to overwrite.")

		zuhs: list[api.Zoo] = ___f_export_to_file.__zuhs

		api.type.pickle_to_file(file, zuhs)

	def ___f_reset_displayhook():
		"""Remove the colored sys.displayhook (The repl result will no longer be colored from this point onwards.)."""
		sys.displayhook = sys.__displayhook__
		return "done"

	def ___f_rank_colors(
		zuhs: list[api.Zoo],
		*,
		include_no_color: bool = True,
		max: int = 10,
	):
		"""Show a leaderboard of zoo colors, which ones are the most used.

		Args:
			zuhs: The list of zuhs (api.Zoo) to operate on, may be a subset you filtered.
			include_no_color: Whether to include the "Use did not use a paintbrush item to select a color yet on this profile" represented by an italic None. Note that the row with "no color" does not count towards the rank column
			max: The max amount of rows to display, use -1 to display up to unlimited amount of rows. 10 by default.
		"""
		counts = Counter(z.color for z in zuhs)

		sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)  # noqa: FURB118

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

			table.add_row(str(i), str(amount), rich.text.Text(f"{color:06x}", style=f"b #{color:06x}") if color is not None else rich.text.Text("None", style="i"))

		rich.print(table)

		if left_from_max := len(sorted_counts) - true_i:
			rich.print(f"[i]{left_from_max} rows were truncated, use max=-1 argument to specify no limit[/]")


if True:  # repl utils

	@instance
	class help(builtins.help.__class__):
		def __or__(self, other):
			return self(other)

		def __ror__(self, other):
			return self(other)

		def __rshift__(self, other):
			return self(other)

		def __rrshift__(self, other):
			return self(other)

		def __lshift__(self, other):
			return self(other)

		def __rlshift__(self, other):
			return self(other)


def run_tui_simple(*zuhs: api.Zoo):
	f_funcs_dict = {k.removeprefix("___f_"): v for k, v in globals().items() if k.startswith("___f_")}

	locals_dict = {
		"zuhs": zuhs,
		**{k: v for k, v in globals().items() if not k.startswith("___")},
		**f_funcs_dict,
	}
	del locals_dict[run_tui_simple.__name__]  # nesting sessions not supported and WILL cause issues.
	___f_export_to_file.__zuhs = zuhs

	def _displayhook_fmt(o):
		return fmt_iterable(o, syntax_highlighting=True, no_implicit_quoteless=True)

	def displayhook(o):
		if o is zuhs:
			print("Rendering the entirety of zuhs may take a long time... consider slicing: zuhs[:3], use Ctrl+C to cancel.")

		if o is not None:
			result = _displayhook_fmt(o)
			print(result)

	sys.displayhook = displayhook

	code.interact(
		banner=f"""
{FMTC.bold}Python {sys.version} on {sys.platform}
{FMTC.NUMBER}(i){FMTC._} {FMTC.bold}Utility functions available: {FMTC.GD_COLON}{f"{FMTC._}{FMTC.bold}, {FMTC._}{FMTC.GD_COLON}".join(x for x in f_funcs_dict)}
{0 * "     "}   {FMTC._} {FMTC.bold}Use {FMTC._}{FMTC.GD_COLON}help{FMTC._}{FMTC.BRACKET}({FMTC._}{FMTC.NONE}<func>{FMTC._}{FMTC.BRACKET}){FMTC._}{FMTC.bold} to get more info.{FMTC._}
>>> len(zuhs)
{_displayhook_fmt(len(zuhs))}
"""[1:-1],
		local=locals_dict,
		exitmsg="",
	)
