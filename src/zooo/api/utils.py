import pathlib as p
from collections.abc import Generator, Iterable

from .type.info import NPCProfileInfo, ProfileInfo, UserInfo


def id_parser(id_strs: Iterable[str]) -> Generator[UserInfo | ProfileInfo | NPCProfileInfo, None, None]:
	"""Parse IDs from a file yielding each immediately, if not able, raise ValueError.

	Comments are allowed:
	```
	507642999992352779 # my user id
	```
	"""

	for s in id_strs:
		if "#" in s:
			s = s.split("#", maxsplit=1)[0]

		s = s.strip()

		last_e = None

		for cls in (NPCProfileInfo, ProfileInfo, UserInfo):
			try:
				yield cls.from_str(s)
				break  # stop trying once one succeeds
			except ValueError as e:
				last_e = e
				continue
		else:
			raise ValueError(f"Unable to parse {s!r} as either of: NPCProfileInfo, ProfileInfo, or UserInfo") from last_e


def id_parser_from_file(path: p.Path):
	"""Yield IDs from a file, if not able, raise ValueError. If there's an issue reading the file let the exception propagate."""

	with path.open() as f:
		yield from id_parser(f)


def profile_sieve(infos: Iterable[UserInfo | ProfileInfo | NPCProfileInfo]) -> tuple[list[UserInfo], list[ProfileInfo | NPCProfileInfo]]:
	"""Sieve out profile infos by type (`UserInfo` vs (`NPC`)`ProfileInfo`)."""

	user_infos = []
	profile_infos = []

	for info in infos:
		if isinstance(info, UserInfo):
			user_infos.append(info)
		elif isinstance(info, ProfileInfo | NPCProfileInfo):
			profile_infos.append(info)
		else:
			raise TypeError(f"Invalid info in infos: {info!r}")

	return user_infos, profile_infos


def profile_info_flattener(infos: UserInfo | ProfileInfo | NPCProfileInfo) -> Generator[UserInfo | NPCProfileInfo]:
	"""For each `ProfileInfo`, replace it with its `UserInfo`, keep `UserInfo`s and `NPCProfileInfo`s as is."""

	for info in infos:
		if isinstance(info, UserInfo | NPCProfileInfo):
			yield info
		elif isinstance(info, ProfileInfo):
			yield info.user
		else:
			raise TypeError(f"Invalid info in infos: {info!r}")
