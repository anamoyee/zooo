import itertools
import logging
import os
import pathlib as p
import random
import sys
import typing as t
from collections.abc import Collection
from enum import StrEnum
from typing import Annotated, Any

import arguably
import nya_fmt as nf
import rich
from nya_result.direct import Result
from rich import print  # ruff:ignore[builtin-import-shadowing]
from rich.syntax import Syntax
from rich.text import Text

from .. import api
from .._version import __version__
from ..api.type.zoo import ThemeID
from .tui import run_tui_simple

term_w = os.get_terminal_size().columns

logging.getLogger("httpx").setLevel(logging.WARNING)

fmt = nf.Formatter(
	include_at_notation=False,
)

if True:  # Helpers

	def _glue_horizontally(*texts: Text) -> Text:
		"""Return texts glued together horizontally, i.e. split at newline and treat each text as a bounding box, place texts next to each other."""
		out_lines: list[Text] = []

		for text in texts:
			lines = text.split("\n")

			while len(out_lines) < len(lines):
				out_lines.append(Text(" " * (out_lines[0].__len__() if out_lines else 0)))

			longest_line_length = max(len(line) for line in lines)

			for i, line in enumerate(lines):
				padded_line = line + Text(" " * max(0, longest_line_length - len(line)))
				out_lines[i] += padded_line

		return Text("\n").join(out_lines)

	def _indent(text: Text, *, indent: Text = Text("\t")) -> Text:
		"""Return text indented by indent, i.e. split at newline and prepend indent to each line."""
		lines = text.split("\n")
		indented_lines = [indent + line for line in lines]
		return Text("\n").join(indented_lines)

	def announce_listed_profiles_pre[T: api.UserInfo](uid: T) -> tuple[int, T]:
		arrow_text = Text.from_markup("[b][white]--> ")
		main_text = Text.from_markup(f"[b][yellow]Fetching profiles of [white]{uid}[yellow]...")

		print(
			text := _glue_horizontally(
				arrow_text,
				main_text,
			),
			end="\r",
		)

		return len(text.plain), uid

	def announce_listed_profiles_post[T: Result[Collection[api.ListedProfile], Any]](
		lps_result: T,
		*,
		uid: api.UserInfo,
		pre_len: int,
	) -> T:
		if lps_result.is_ok:
			text = _glue_horizontally(
				Text.from_markup("[b][white]--> "),
				Text.from_markup(f"[b][green]Fetched profiles of [white]{uid}[/]."),
			)

		else:
			e = lps_result.unwrap_err()

			text = _glue_horizontally(
				Text.from_markup("[b][white]==> "),
				Text().join((
					Text.from_markup(f"[b][red]Failed to fetch profiles of [white]{uid}[/].\n"),
					_indent(
						Text().join((
							fmt(e.__class__),
							Text(": ", style=fmt.styles.punctuation),
							Text(str(e), style=fmt.styles.string),
						)),
						indent=Text("| ", style=fmt.styles.false),
					),
				)),
			)

		post_len = len(text.plain)

		text += Text(" " * max(0, pre_len - post_len))  # pad with spaced, so that the below print is entirely overwritten by the above one.
		# do not use f'{s:<{pre_len}}' as this ignores the markup tags.

		print(text)

		return lps_result

	def announce_zoo_pre[T: api.ProfileInfo | api.NPCProfileInfo](pid: T) -> tuple[int, T]:
		arrow_text = Text.from_markup("[b][white]--> ")
		main_text = Text.from_markup(f"[b][yellow]Fetching profile [white]{pid}[yellow]...")

		print(
			text := _glue_horizontally(
				arrow_text,
				main_text,
			),
			end="\r",
		)

		return len(text.plain), pid

	def announce_zoo_post[T: Result[api.Zoo, Any]](
		zoo_result: T,
		*,
		pid: api.ProfileInfo | api.NPCProfileInfo,
		pre_len: int,
	) -> T:
		if zoo_result.is_ok:
			text = _glue_horizontally(
				Text.from_markup("[b][white]--> "),
				Text.from_markup(f"[b][green]Fetched profile [white]{pid}[/]."),
			)

		else:
			e = zoo_result.unwrap_err()

			text = _glue_horizontally(
				Text.from_markup("[b][white]==> "),
				Text().join((
					Text.from_markup(f"[b][red]Failed to fetch profile [white]{pid}[/].\n"),
					_indent(
						Text().join((
							fmt(e.__class__),
							Text(": ", style=fmt.styles.punctuation),
							Text(str(e), style=fmt.styles.string),
						)),
						indent=Text("| ", style=fmt.styles.false),
					),
				)),
			)

		post_len = len(text.plain)

		text += Text(" " * max(0, pre_len - post_len))  # pad with spaced, so that the below print is entirely overwritten by the above one.
		# do not use f'{s:<{pre_len}}' as this ignores the markup tags.

		print(text)

		return zoo_result


@arguably.command
async def __root__(
	*,
	ids_path: p.Path | None = None,
	import_path: p.Path | None = None,
	export_path: p.Path | None = None,
	ix_sync: bool = False,
	bake_ids: Annotated[int, arguably.arg.count()] = 0,
	gui: bool = False,
	cookie: str | None = None,
	tcr_c_callsite: bool = False,
):
	r"""Fetch profile/s from either the internet (gdcolon.com/zoo) or from a locally pickled save object. When fetching finishes, get dropped into an interactive python sessions with a few utility functions to easily analyze your data.

	Args:
		ids_path: [-f] path to a file that contains newline-separated discord or profile ids.
		import_path: [-i] path to a file containing the previously -x/--exported data
		export_path: [-x] path to a file to export the data to
		ix_sync: [-X] if set, when either of -x or -i is provided, set other one to the former. If both or none are provided, raise an error.
		bake_ids: [-B] [This will rearrange the file potentialy leading to data loss!] In the provided ids_file, pre-fetch and replace all user IDs ("1234") with their respective profile IDs ("1234_fox\n1234_cat"), this will speed up fetching later, but will cause not to find all profiles if the user makes a new one, in this case: bake again. Pass this twice to *only bake* (do not enter interactive mode afterwards)
		gui: [-G] Use the ImGui (dearpygui) gui view instead of the default drop-into-repl
		cookie: [-C] The zoo cookie to use for optional authentication. To obtain the cookie, go to https://gdcolon.com/zoo, log in with discord, open developer tools (CTRL+SHIFT+I or F12, depends on the web browser you use), in the console tab type `document.cookie`, paste the part inbetween quotes as the value of this parameter, or as value of the ZOOO_COOKIE environment variable.
		tcr_c_callsite: does nothing, just for tcrutils.console	compatibility

	Raises:
		ValueError: if both or none of -x/--export and -i/--import are provided when --ix-sync is set.
	"""

	if not arguably.is_target():
		return

	if gui:
		from .gui import run_gui

	cookie = cookie_from_param_or_env(cookie, required=False)

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
		print("[b][red]Cannot bake if there's no ids_path to bake with! hmph ( •̀ ⤙ •́ )")
		exit(1)

	if bake_ids:
		profiles = api.utils.profile_info_flattener(profiles)

	user_infos, profile_infos = api.utils.profile_info_sieve(profiles)

	async with api.Client(api.Client.make_httpx_client(cookie)) as zcl:
		announcing_uids = (announce_listed_profiles_pre(uid) for uid in set(user_infos))

		results = (
			(
				uid,
				announce_listed_profiles_post(
					await zcl.fetch_listed_profiles(
						uid,
					),
					uid=uid,
					pre_len=pre_len,
				),
			)
			for pre_len, uid in announcing_uids
		)

		_lps_ok = []

		async for _, res in results:
			if res.is_ok:
				_lps_ok.append(res.unwrap())

		_lps_ok_flattened = [
			lp  #
			for lp_collection_result in _lps_ok
			for lp in lp_collection_result
		]

		_lps1, _lps2 = itertools.tee(_lps_ok_flattened, 2)

		lps_viewable = (lp for lp in _lps1 if lp.viewable)
		lps_unviewable = (lp for lp in _lps2 if not lp.viewable)

		profile_infos.extend(lp.id for lp in lps_viewable)

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

		announcing_pids = (announce_zoo_pre(pid) for pid in set(profile_infos))

		zuh_results = (
			(
				pid,
				announce_zoo_post(
					await zcl.fetch_zoo(
						pid  #
					),
					pid=pid,
					pre_len=pre_len,
				),
			)
			for pre_len, pid in announcing_pids
		)

		zuhs = []
		_zuh_results_err_map = {}

		async for pid, res in zuh_results:
			if res.is_ok:
				zuhs.append(res.unwrap())
			else:
				_zuh_results_err_map[pid] = res.unwrap_err()

	for pid, err_zuh in _zuh_results_err_map.items():
		# todo: switch to an async generator approach where the error gets printed inline, some sort of wrapper-async-generator that does the printing.
		print(f"[b][red]    Failed to fetch zoo for [white]{pid}[red]! Error: {err_zuh!r}")

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

	if gui:
		run_gui(*zuhs_including_imported_zuhs)
	else:
		run_tui_simple(*zuhs_including_imported_zuhs)


class PublicOrPrivateState(StrEnum):
	"""An enum to nudge arguably to require an explicit declaration of privateness for a command argument."""

	PUBLIC = "public"
	PRIVATE = "private"

	def is_public(self) -> bool:
		"""Return True if the state is PUBLIC, False if PRIVATE."""

		match self:
			case PublicOrPrivateState.PUBLIC:
				return True
			case PublicOrPrivateState.PRIVATE:
				return False
			case _:
				msg = f"Invalid PublicOrPrivateState value: {self!r}"
				raise ValueError(msg)


@t.overload
def cookie_from_param_or_env(cookie: str | None, *, required: t.Literal[True] = ...) -> str: ...


@t.overload
def cookie_from_param_or_env(cookie: str | None, *, required: t.Literal[False] = False) -> str | None: ...


def cookie_from_param_or_env(cookie: str | None, *, required: bool = True) -> str | None:
	"""Get a cookie from either the provided parameter or the environment variable ZOOO_COOKIE.

	If both are provided, raise an error.
	If neither are provided, raise an error if required is True, otherwise return None.

	Args:
		cookie: The cookie provided as a parameter.
		required: If True, raise an error if no cookie is found. If False, return None if no cookie is found.

	Returns:
		The cookie to use for the command with 'zoo=' prefix stripped, if found.

	Raises:
		SystemExit: If the arguably.error() path was chosen and it exits the program with an error message.
	"""  # ruff: ignore[docstring-extraneous-exception, docstring-missing-exception]
	env_cookie = os.environ.get("ZOOO_COOKIE")

	if (
		sum((
			cookie is not None,
			env_cookie is not None,
		))
		> 1
	):
		msg_0 = "Ambiguous cookie: Both the parameter and the environment variable ZOOO_COOKIE provide a cookie. Please provide only one."
		arguably.error(msg_0)
		raise ValueError("unreachable")  # ruff: ignore[raw-string-in-exception]

	if cookie is not None:
		return cookie.removeprefix("zoo=")

	if env_cookie is not None:
		return env_cookie.removeprefix("zoo=")

	if not required:
		return None

	msg_1 = "No cookie provided: Please provide a cookie either through the parameter or the environment variable ZOOO_COOKIE."
	arguably.error(msg_1)
	raise ValueError("unreachable")  # ruff: ignore[raw-string-in-exception]


@arguably.command
async def profile_settings(
	profile: str | None,
	*,
	profile_visibility: PublicOrPrivateState | None,
	cosmetics_visibility: PublicOrPrivateState | None,
	theme: ThemeID | None,
	skip_empty_requests: bool = False,
	cookie: str | None = None,
) -> None:
	"""Change whether this profile is set to public via the web API (`profileSettings` endpoint).

	Args:
		profile: The profile ID to change the setting for.
		profile_visibility: [-v] The visibility state of the profile.
		cosmetics_visibility: [-c] The visibility state of the cosmetics.
		theme: [-t] The theme to use for the profile.
		skip_empty_requests: [-S] if set, if no settings are provided, skip sending the request entirely, return immediately. Otherwise send a "no changes requested" request e.g. to validate the cookie (the default).
		cookie: [-C] The authentication cookie to use for the command. Alternatively use the ZOOO_COOKIE environment variable (recommended). If both or neither are provided an error is raised.
	"""  # ruff: ignore[docstring-missing-exception]

	if profile is None:  # sidestepping bug in arguably, subcommands may be invoked without their required arguments apparently...?
		arguably.error("The profile ID must be provided with the -p/--profile option.")
		assert profile is not None  # shut up type checkers

	cookie = cookie_from_param_or_env(cookie)

	try:
		profile_info = api.ProfileInfo.from_str(profile)
	except ValueError as e:
		msg = "Invalid profile ID string provided, please provide a valid profile ID in the form of `<user_id>_<profile_name>`, e.g. 123456789_fox."
		msg += f"\n  Further details: {e}"
		arguably.error(msg)

	payload_dict = api.Client.TargetSettingsTD()

	if profile_visibility is not None:
		payload_dict["profile_visibility"] = profile_visibility.is_public()

	if cosmetics_visibility is not None:
		payload_dict["cosmetics_visibility"] = cosmetics_visibility.is_public()

	if theme is not None:
		payload_dict["theme"] = theme

	async with api.Client(api.Client.make_httpx_client(cookie)) as zcl:
		result = await zcl.change_settings(
			profile_info,
			**payload_dict,
			send_empty_requests=not skip_empty_requests,
		)

	if result.is_ok:
		assert result.unwrap() == b"cool and good"
		return

	e = result.unwrap_err()

	rich.console.Console(highlight=False, file=sys.stderr).print(
		Text().join((
			Text("Failed to change settings for profile ", style="bold red"),
			fmt(profile_info),
			Text("\n"),
			fmt(e.__class__),
			Text(": ", style=fmt.styles.punctuation),
			Text(str(e), style=fmt.styles.string),
		))
	)
	raise SystemExit(1)


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
