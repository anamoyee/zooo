import pathlib as p
from collections.abc import Generator, Iterable

from .type.info import NPCProfileInfo, ProfileInfo, UserInfo


def parse_ids(id_strs: Iterable[str]) -> Generator[UserInfo | ProfileInfo | NPCProfileInfo, None, None]:
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


def parse_ids_from_file(path: p.Path):
	"""Yield IDs from a file, if not able, raise ValueError. If there's an issue reading the file let the exception propagate."""

	with path.open() as f:
		yield from parse_ids(f)


def sieve_profiles(values: Iterable[UserInfo | ProfileInfo | NPCProfileInfo]) -> tuple[list[UserInfo], list[ProfileInfo | NPCProfileInfo]]:
	"""Sieve out profiles by type (User vs Profile)."""

	user_infos = []
	profile_infos = []

	for value in values:
		if isinstance(value, UserInfo):
			user_infos.append(value)
		elif isinstance(value, ProfileInfo | NPCProfileInfo):
			profile_infos.append(value)
		else:
			raise TypeError(f"Invalid value in profiles: {value!r}")

	return user_infos, profile_infos
