import asyncio
import os
import pathlib as p
import sys

import arguably
from rich.traceback import install as _rich_traceback_install
from tcrutils.console import c

from .. import api
from .._version import __version__
from .tui import App

### PLAN ###
# Do not add *pos args to __root__ - handle everything in a separate tab setup in textual, other tabs are disabled until pressed a button or something
#  - but do add --keyword arguments
#  - add --autostart or something argument that would click the aformentioned button right away
# Bring over the lite command from zms


@arguably.command
async def __root__(
	*,
	ids_file: p.Path | None = None,
	ansi_color: bool = False,
	no_mouse_support: bool = False,
	tcr_c_callsite: bool = False,
):
	"""TODO: insert description here when making the README.md or if you forgot right fucking now.

	Args:
		ids_file: [-f] path to a file that contains newline-separated discord or profile ids.
		ansi_color: [-A] run the app in reduced color palette mode.
		no_mouse_support: [-M] disable mouse support for the app (by default mouse is supported).
		tcr_c_callsite: does nothing, just for tcrutils.console	compatibility
	"""

	if ids_file is None:
		ids_file = p.Path("ids.txt")

	profiles = api.utils.parse_ids_from_file(ids_file)

	user_infos, profile_infos = api.utils.sieve_profiles(profiles)

	async with api.Client() as zcl:
		lps = (await zcl.fetch_profiles_mass(*set(user_infos))).ok_values()

		profile_infos.extend(lp.id for lp in lps)

		print()  # Add a newline between 'fetching profiles of $x' and 'fetching profie $x'
		zuhs = (await zcl.fetch_zoo_mass(*set(profile_infos))).ok_values()

	await App(
		*zuhs,
		ansi_color=ansi_color,
	).run_async(
		mouse=not no_mouse_support,
	)


# bring over the docstring from zms


def main():
	term_w = os.get_terminal_size().columns

	_rich_traceback_install(width=term_w, code_width=term_w)

	sys.modules["__main__"].__version__ = __version__  # arguably version fix
	arguably.run(
		name="zooo",
		version_flag=("-V", "--version"),
		strict=True,
		show_defaults=False,
		show_types=False,
	)
