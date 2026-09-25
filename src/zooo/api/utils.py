import pathlib as p
from collections.abc import Generator, Iterable

from .type.info import NPCProfileInfo, ProfileInfo, UserInfo

type Json = dict[str, Json] | list[Json] | str | int | float | bool | None


def profile_info_parse_from_str(s: str, /) -> UserInfo | ProfileInfo | NPCProfileInfo:
	"""Parse IDs from a string, if not able raise ValueError.

	Comments are allowed:
	```
	507642999992352779  # my user id
	```

	Returns:
		- `UserInfo` if the ID is a user ID.
		- `ProfileInfo` if the ID is a profile ID.
		- `NPCProfileInfo` if the ID is an NPC profile ID.

	Raises:
		ValueError: if any of the IDs is not a valid `UserInfo`, `ProfileInfo` or `NPCProfileInfo`.
	"""

	if "#" in s:
		s = s.split("#", maxsplit=1)[0]

	s = s.strip()

	for cls in (NPCProfileInfo, ProfileInfo, UserInfo):
		try:
			return cls.from_str(s)
		except ValueError:
			continue

	msg_1 = f"Unable to parse {s!r} as either of: NPCProfileInfo, ProfileInfo, or UserInfo."
	raise ValueError(msg_1)


def profile_infos_parse_from_file(path: p.Path) -> Generator[UserInfo | ProfileInfo | NPCProfileInfo]:
	"""Yield IDs from a file, if not able, raise ValueError. If there's an issue reading the file let the exception propagate."""

	with path.open(encoding="utf-8") as f:
		yield from (profile_info_parse_from_str(line) for line in f)


def profile_info_sieve(
	infos: Iterable[UserInfo | ProfileInfo | NPCProfileInfo],
) -> tuple[
	list[UserInfo],
	list[ProfileInfo | NPCProfileInfo],
]:
	"""Sieve out profile infos by type (`UserInfo` vs (`NPC`)`ProfileInfo`).

	Returns:
		A tuple of two lists:
			- The first list contains all `UserInfo` instances.
			- The second list contains all `ProfileInfo` and `NPCProfileInfo` instances.

	Raises:
		TypeError: if any of the infos is not a `UserInfo`, `ProfileInfo` or `NPCProfileInfo`.
	"""

	user_infos = []
	profile_infos = []

	for info in infos:
		if isinstance(info, UserInfo):
			user_infos.append(info)
		elif isinstance(info, ProfileInfo | NPCProfileInfo):
			profile_infos.append(info)
		else:
			msg = f"Invalid info in infos: {type(info).__name__!r}"
			raise TypeError(msg)

	return user_infos, profile_infos


def profile_info_flattener(infos: Iterable[UserInfo | ProfileInfo | NPCProfileInfo]) -> Generator[UserInfo | NPCProfileInfo]:
	"""For each `ProfileInfo`, replace it with its `UserInfo`, keep `UserInfo`s and `NPCProfileInfo`s as is.

	Yields:
		- for `UserInfo` and `NPCProfileInfo`: return same object as is.
		- for `ProfileInfo`: `UserInfo` extracted out of each `ProfileInfo`.

	Raises:
		TypeError: if any of the infos is not a `UserInfo`, `ProfileInfo` or `NPCProfileInfo`.
	"""

	for info in infos:
		if isinstance(info, UserInfo | NPCProfileInfo):
			yield info
		elif isinstance(info, ProfileInfo):
			yield info.user
		else:
			msg = f"Invalid info in infos: {info!r}"
			raise TypeError(msg)
