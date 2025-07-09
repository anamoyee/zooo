import itertools
import logging
import os
import pathlib as p
import random
import sys
from typing import Annotated

import arguably
import rich
from rich import print
from rich.syntax import Syntax
from tcrutils.console import c

from .. import api
from .._version import __version__
from .tui import App

# TODO:
# Do not add *pos args to __root__ - handle everything in a separate tab setup in textual, other tabs are disabled until pressed a button or something
#  - but do add --keyword arguments
#  - add --autostart or something argument that would click the aformentioned button right away
# Bring over the lite command from zms

# if profiles fail to load, give a red toast in Textual app


@arguably.command
async def __root__(
	*,
	ids_path: p.Path | None = None,
	ansi_color: bool = False,
	no_mouse_support: bool = False,
	import_path: p.Path | None = None,
	export_path: p.Path | None = None,
	ix_sync: bool = False,
	bake_ids: Annotated[int, arguably.arg.count()] = 0,
	tcr_c_callsite: bool = False,
):
	"""TODO: insert description here when making the README.md or if you forgot right fucking now.

	Args:
		ids_path: [-f] path to a file that contains newline-separated discord or profile ids.
		ansi_color: [-A] run the app in reduced color palette mode.
		no_mouse_support: [-M] disable mouse support for the app (by default mouse is supported).
		import_path: [-i] path to a file containing the previously -x/--exported data
		export_path: [-x] path to a file to export the data to
		ix_sync: [-X] if set, when either of -x or -i is provided, set other one to the former. If both or none are provided, raise an error.
		bake_ids: [-B] [This will rearrange the file potentialy leading to data loss!] In the provided ids_file, pre-fetch and replace all user IDs ("1234") with their respective profile IDs ("1234_fox\\n1234_cat"), this will speed up fetching later, but will cause not to find all profiles if the user makes a new one, in this case: bake again. Pass this twice to *only bake* (do not enter interactive mode afterwards)
		tcr_c_callsite: does nothing, just for tcrutils.console	compatibility
	"""

	if ix_sync:
		if import_path is None and export_path is None:
			raise ValueError("One of -x/--export or -i/--import must be provided if --ix-sync is set.")

		if import_path is not None and export_path is not None:
			raise ValueError("Only one of -x/--export or -i/--import can be provided if --ix-sync is set.")

		if import_path is None:
			import_path = export_path
		else:
			export_path = import_path

	if ids_path is None:
		ids_path = p.Path("ids.txt")

		if import_path is not None and not ids_path.exists():
			ids_path = None

	if ids_path:
		profiles = api.utils.IDParserFromFile(ids_path)
	else:
		profiles = []

	if import_path is not None:
		try:
			imported: list[api.Zoo] = api.type.unpickle_from_file(import_path)
		except FileNotFoundError:
			if import_path == import_path:
				print(
					f"[b][red]Import file [white]{import_path.name}[/] doesnt exist, but export_path == import_path, assuming this is the first run or the file was deleted and therefore import as a source is skipped."
				)
				imported = []
			else:
				print(f"[b][red]Import file [white]{import_path.name}[/] is missing, aborting...[/]")
				exit(1)

		except Exception as e:
			e.add_note(
				3 * "\nThere was an error loading your profiles from this export, please re-export them or if you can't and really want the data try using the same version of zooo as you imported."
			)
			raise
	else:
		imported = []

	if bake_ids and ids_path is None:
		print("[b][red]Cannot bake cookies while there's no ids_path to bake with! hmph ( •̀ ⤙ •́ )")
		exit(1)

	if bake_ids:
		profiles = api.utils.ProfileInfoFlattener(profiles)

	user_infos, profile_infos = api.utils.ProfileSieve(profiles)

	async with api.Client() as zcl:
		lps = (await zcl.fetch_profiles_mass(*set(user_infos))).ok_values()

		_lps1, _lps2 = itertools.tee(lps, 2)

		lps = (lp for lp in _lps1 if lp.viewable)
		lps_unviewable = (lp for lp in _lps2 if not lp.viewable)

		profile_infos.extend(lp.id for lp in lps)

		if bake_ids:
			print()
			print(f"[b][#ff8000]Baking {'cookies' if random.randint(0, 100) == 69 else 'IDs'}... ", end="")

			before = ids_path.read_text()

			ids_path.write_text(
				after := (
					"\n".join(
						sorted(str(prof_info) for prof_info in profile_infos),
					).strip()
					+ "\n"
				)
			)

			before, after = before.strip(), after.strip()

			print("[b][#ff8000]Done! 🍪")

			if before != after:
				print("\n[b][#ff8000]Before 🤮")
				print(Syntax(before, "txt"))

				print("\n[b][#ff8000]After ✨")
				print(Syntax(after, "txt"))
			else:
				print("[b][#ff8000]No changes after baking.")

			if bake_ids >= 2:
				return

		imported_profile_infos: list[api.UserInfo | api.ProfileInfo] = []
		for info in profile_infos:
			if info in (x.id for x in imported):
				imported_profile_infos.append(info)

		profile_infos = [info for info in profile_infos if info not in imported_profile_infos]

		print()  # Add a newline between 'fetching profiles of $x' and 'fetching profie $x'

		_any_unviewable_profiles = False
		for unv_lp in lps_unviewable:
			_any_unviewable_profiles = True
			print(f"[b][yellow]    The profile [white]{unv_lp.id}[yellow] is not viewable, skipping...")

		if _any_unviewable_profiles:
			if bake_ids:
				print(f"[b][yellow]    [white]-->[/] The next time you run zooo without baking, this will be fixed!")
			else:
				print(f"[b][yellow]    [white]-->[/] Consider [i white]baking[/] your IDs with [white]--bake[/]")

		zuhs = (await zcl.fetch_zoo_mass(*set(profile_infos))).ok_values()

	zuhs_including_imported_zuhs = [*zuhs, *imported]

	if imported_profile_infos or export_path:
		print()  # add a newline before the imports, if any

	if imported_profile_infos:
		print(f"[b][white]--> [yellow]Imported [white]{len(imported_profile_infos)} [yellow]profiles from [white]{import_path.name}[yellow]!")

	if export_path:
		api.type.pickle_to_file(export_path, zuhs_including_imported_zuhs)
		print(f"[b][white]<-- [yellow]Exported [white]{len(zuhs_including_imported_zuhs)} [yellow]profiles to [white]{export_path.name}[yellow]!")

	await App(
		*zuhs_including_imported_zuhs,
		ids_file=ids_path,
		ansi_color=ansi_color,
	).run_async(
		mouse=not no_mouse_support,
	)


# bring over the docstring from zms


def main():
	import rich.logging
	from rich.traceback import install as _rich_traceback_install

	term_w = os.get_terminal_size().columns

	logging.basicConfig(
		format="%(message)s",
		datefmt="[%X]",
		handlers=[
			rich.logging.RichHandler(
				rich_tracebacks=True,
				tracebacks_show_locals=True,
				tracebacks_width=term_w,
				tracebacks_code_width=term_w,
			)
		],
	)

	_rich_traceback_install(
		width=term_w,
		code_width=term_w,
	)

	sys.modules["__main__"].__version__ = __version__  # arguably version fix
	arguably.run(
		name="zooo",
		version_flag=("-V", "--version"),
		strict=True,
		show_defaults=False,
		show_types=False,
		max_width=term_w - 2,
	)
