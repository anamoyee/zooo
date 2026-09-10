if True:  # bootstrap rich traceback & logging first, so any syntax errors in other files also work  # ruff:ignore[non-empty-init-module]
	import logging
	import os

	import rich.logging
	from rich.traceback import install as _rich_traceback_install

	term_w = os.get_terminal_size().columns

	logging.basicConfig(
		level=logging.INFO,
		format="%(message)s",
		datefmt="[%X]",
		handlers=[
			rich.logging.RichHandler(
				rich_tracebacks=True,
				tracebacks_show_locals=False,
				tracebacks_width=term_w,
				tracebacks_code_width=term_w,
			)
		],
	)

	_rich_traceback_install(
		width=term_w,
		code_width=term_w,
		show_locals=False,
	)


from .cli import main as main
