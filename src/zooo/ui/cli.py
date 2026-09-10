import itertools
import os
import pathlib as p
import random
import sys
from typing import Annotated

import arguably

term_w = os.get_terminal_size().columns
from rich import print  # ruff:ignore[builtin-import-shadowing]
from rich.syntax import Syntax

from .. import api
from .._version import __version__
from .tui import run_tui_simple


@arguably.command
async def __root__(
	*,
	ids_path: p.Path | None = None,
	import_path: p.Path | None = None,
	export_path: p.Path | None = None,
	ix_sync: bool = False,
	bake_ids: Annotated[int, arguably.arg.count()] = 0,
	tcr_c_callsite: bool = False,
):
	r"""Fetch profile/s from either the internet (gdcolon.com/zoo) or from a locally pickled save object. When fetching finishes, get dropped into an interactive python sessions with a few utility functions to easily analyze your data.

	Args:
		ids_path: [-f] path to a file that contains newline-separated discord or profile ids.
		import_path: [-i] path to a file containing the previously -x/--exported data
		export_path: [-x] path to a file to export the data to
		ix_sync: [-X] if set, when either of -x or -i is provided, set other one to the former. If both or none are provided, raise an error.
		bake_ids: [-B] [This will rearrange the file potentialy leading to data loss!] In the provided ids_file, pre-fetch and replace all user IDs ("1234") with their respective profile IDs ("1234_fox\n1234_cat"), this will speed up fetching later, but will cause not to find all profiles if the user makes a new one, in this case: bake again. Pass this twice to *only bake* (do not enter interactive mode afterwards)
		tcr_c_callsite: does nothing, just for tcrutils.console	compatibility

	Raises:
		ValueError: if both or none of -x/--export and -i/--import are provided when --ix-sync is set.
	"""

	if ix_sync:
		if import_path is None and export_path is None:
			msg_0 = "One of -x/--export or -i/--import must be provided if --ix-sync is set."
			raise ValueError(msg_0)

		if import_path is not None and export_path is not None:
			msg_1 = "Only one of -x/--export or -i/--import can be provided if --ix-sync is set."
			raise ValueError(msg_1)

		if import_path is None:
			import_path = export_path
		else:
			export_path = import_path

	if ids_path is None:
		ids_path = p.Path("ids.txt")

		if import_path is not None and not ids_path.exists():
			ids_path = None

	profiles = api.utils.profile_infos_parse_from_file(ids_path) if ids_path else []

	if import_path is not None:
		try:
			imported: list[api.Zoo] = api.type.unpickle_from_file(import_path)
		except FileNotFoundError:
			if export_path == import_path:
				print(
					f"[b][red]Import file [white]{import_path.name}[/] doesnt exist, but export_path == import_path, assuming this is the first run or the file was deleted and therefore import as a source is skipped."
				)
				imported = []
			else:
				print(f"[b][red]Import file [white]{import_path.name}[/] is missing, aborting...[/]")
				exit(1)

		except Exception as e:
			e.add_note(
				3
				* "\nThere was an error loading your profiles from this export, please re-export them or if you can't and really want the data try using the same version of zooo as you imported."
			)
			raise
	else:
		imported = []

	if bake_ids and ids_path is None:
		print("[b][red]Cannot bake cookies while there's no ids_path to bake with! hmph ( •̀ ⤙ •́ )")
		exit(1)

	if bake_ids:
		profiles = api.utils.profile_info_flattener(profiles)

	user_infos, profile_infos = api.utils.profile_info_sieve(profiles)

	async with api.Client() as zcl:
		lps = (await zcl.fetch_profiles_mass(*set(user_infos))).ok_values_flattened()

		_lps1, _lps2 = itertools.tee(lps, 2)

		lps = (lp for lp in _lps1 if lp.viewable)
		lps_unviewable = (lp for lp in _lps2 if not lp.viewable)

		profile_infos.extend(lp.id for lp in lps)

		if bake_ids:
			assert ids_path is not None  # nudge typecheckers, checked manually above, look for 'if bake_ids and ids_path is None:'

			print()
			print(f"[b][#ff8000]Baking {"cookies" if random.randint(0, 100) == 69 else "IDs"}... ", end="")

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

		imported_profile_infos = [
			info  #
			for info in profile_infos
			if info in (x.id for x in imported)
		]

		profile_infos = [
			info  #
			for info in profile_infos
			if info not in imported_profile_infos
		]

		if profile_infos:
			print()  # Add a newline between 'fetching profiles of $x' and 'fetching profie $x'

		_any_unviewable_profiles = False
		for unv_lp in lps_unviewable:
			_any_unviewable_profiles = True
			print(f"[b][yellow]    The profile [white]{unv_lp.id}[yellow] is not viewable, skipping...")

		if _any_unviewable_profiles:
			if bake_ids:
				print("[b][yellow]    [white]-->[/] The next time you run zooo without baking, this will be fixed!")
			else:
				print("[b][yellow]    [white]-->[/] Consider [i white]baking[/] your IDs with [white]--bake[/]")

		zuhs = (await zcl.fetch_zoo_mass(*set(profile_infos))).ok_values()

	zuhs_including_imported_zuhs = [*zuhs, *imported]

	if imported_profile_infos or export_path:
		print()  # add a newline before the imports, if any (1/2)

	if imported_profile_infos:
		assert import_path is not None
		print(f"[b][white]--> [yellow]Imported [white]{len(imported_profile_infos)} [yellow]profiles from [white]{import_path.name}[yellow]!")

	if export_path:
		api.type.pickle_to_file(export_path, zuhs_including_imported_zuhs)
		print(f"[b][white]<-- [yellow]Exported [white]{len(zuhs_including_imported_zuhs)} [yellow]profiles to [white]{export_path.name}[yellow]!")

	if imported_profile_infos or export_path:
		print()  # add a newline before the imports, if any (2/2)

	run_tui_simple(*zuhs_including_imported_zuhs)


def main():
	sys.modules["__main__"].__version__ = __version__  # arguably version fix  # ty: ignore[unresolved-attribute]
	arguably.run(
		name="zooo",
		version_flag=("-V", "--version"),
		strict=True,
		show_defaults=False,
		show_types=False,
		max_width=term_w - 2,
	)
