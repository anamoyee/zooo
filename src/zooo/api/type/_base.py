import pickle
from pathlib import Path
from typing import Any

import pydantic as pd
from pydantic import BaseModel as __BaseModel
from pydantic import Field

from ..error import add_helpful_note_to_validation_error

_IGNORE_KEYS: frozenset[str] = frozenset({
	"_apiKey",  # useless
	"userID",  # double information (already contained in id)
	"profileID",  # double information (already contained in id)
})
_UPPERCASE_KEY_SUBSTRINGS: frozenset[str] = frozenset({"id", "xp"})


def snake_to_camel(
	s: str,
	always_uppercase: frozenset[str] = frozenset({"id"}),
	*,
	unless_str_fully_in_always_uppercase: bool = False,
) -> str:
	"""Convert a `snake_case` string to `camelCase`.

	Args:
		s: The `snake_case` string to convert.
		always_uppercase: A set of substrings that should always be converted to uppercase in the resulting `camelCase` string. (think: ID, XP, etc. which would without this be converted to Id, Xp, etc.)
		unless_str_fully_in_always_uppercase: If True, the entire string will not be converted to uppercase even if it is in the `always_uppercase` set. (think: "userID" but not "ID", instead "id")

	Returns:
		The string in `camelCase`.
	"""

	if unless_str_fully_in_always_uppercase and s.lower() in always_uppercase:
		return s

	words = s.split("_")
	converted = words[0] + "".join(word.title() for word in words[1:])

	for word in always_uppercase:
		converted = converted.replace(word.title(), word.upper())

	return converted


class _BM(__BaseModel):
	raw_json: dict = Field(default_factory=dict, exclude=True, repr=False)

	def __init__(self, **data: Any):
		data = {k: v for k, v in data.items() if k not in _IGNORE_KEYS}
		data = {snake_to_camel(k): v for k, v in data.items()}
		try:
			super().__init__(**data)
		except pd.ValidationError as e:
			add_helpful_note_to_validation_error(e)

			raise

		self.raw_json = data

	def __repr__(self):  # Classic repr
		class_name = self.__class__.__name__
		fields_str = " ".join(f"{key}={value!r}" for key, value in self.__dict__.items())
		return f"{class_name}({fields_str})"

	class Config:
		extra = "forbid"
		"""If the API gets updated it'd be better to raise an error i guess"""
		arbitrary_types_allowed = True
		"""Required for tcr.HexInt"""
		alias_generator = lambda x: snake_to_camel(x, always_uppercase=_UPPERCASE_KEY_SUBSTRINGS, unless_str_fully_in_always_uppercase=True)  # noqa: E731
		"""For now let's not worry about the '_apiKey' key, ignoring it since it's useless so it's just not included in the profile object."""


if True:  # Functionality/parts/mixin classes
	# classes here should not define methods like _MEmoji.is_unicode(), as it would be ambigous what is unicode,
	# since the name of the later subclass will not make it obvious that the is the `.emoji` field being checked
	# for unicode. Prefer something like `.is_emoji_unicode()`

	class _MEmoji:
		"""Lets pydantic models inherit `.emoji` and `.emoji`-related methods."""

		emoji: str
		"""The emoji of this object."""

		def is_emoji_unicode(self) -> bool:
			"""Whether or not the emoji of this item is a unicode emoji (aka: NOT a discord custom emoji).

			Returns:
				is_emoji_unicode: True if the emoji is a unicode emoji, False if it's a discord custom emoji.
			"""
			return not self.emoji.startswith("<")

	class _MObtainable(_BM):
		"""Represents obtainable object in Zoo, not used standalone, only subclassed."""

		obtained: bool = True
		"""Whether or not this item has been obtained in this profile, if False it means it has been derived either due to direct request or parsing (that is: This profile does not have this item/animal/cosmetic/etc. and if possible, it's amount is 0, if there's no 'amount' field you have to rely on this field)."""


# todo: convert pickling to use json
def pickle_to_file(path: Path, o: Any) -> None:
	path.write_bytes(pickle.dumps(o))


def unpickle_from_file(path: Path) -> Any:
	return pickle.loads(path.read_bytes())
