from __future__ import annotations

import builtins
import code
import sys
from typing import TYPE_CHECKING, Any

import rich.markup
from rich.console import Console

if TYPE_CHECKING:
	from rich.text import Text

	from ... import api

from nya_fmt import Formatter

from . import f_funcs


def render_rich_text_into_ansi_str(text: Text) -> str:
	console = Console(
		# force_terminal=True,
		# color_system="truecolor",
	)

	with console.capture() as capture:
		console.print(text, end="")

	return capture.get()


def run_tui_simple(*zuhs: api.Zoo):
	# f_funcs_dict = {k.removeprefix("___f_"): v for k, v in globals().items() if k.startswith("___f_")}

	locals_dict = {
		# "help": __AugmentedHelpType(),  # todo: instead of this, where help was just builtin help but accepted __lshift__, __or__, etc., make nya_fmt natively handle those functions, possibly register format providers or just make builtin format provider for function which reads docstring.
		"zuhs": zuhs,
		# **{k: v for k, v in globals().items() if not k.startswith("___")},
		**f_funcs.REGISTERED.get_dict(),
	}

	fmt = Formatter(no_quoteless_str=True)

	def displayhook(o: Any):
		# intentionally not doing a `if o is None: return`, because i want to keep it printing None, for less confusion

		result = fmt(o)
		rich.print(result)
		builtins._ = o  # ty: ignore[unresolved-attribute]

	sys.displayhook = displayhook

	code.interact(
		banner=render_rich_text_into_ansi_str(
			rich.markup.render(
				f"""
[b]Python {sys.version} on {sys.platform}
[blue](i)[/blue] Utility functions available: {", ".join(f"[orange1]{rich.markup.escape(name)}[/]" for name in f_funcs.REGISTERED.get_dict())}
{0 * "     "}    Use [orange1]help[/][cyan]([/][orange1]func[/][cyan])[/] to get more info.[/b]
>>> len(zuhs){setattr(builtins, "_", len_zuhs := len(zuhs)) or ""}

"""[1:-1]
			)
		)
		+ render_rich_text_into_ansi_str(fmt(len_zuhs)),
		local=locals_dict,
		exitmsg="",
	)
