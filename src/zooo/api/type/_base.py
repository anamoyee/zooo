import pickle
import re as _regex
from collections.abc import MutableMapping as _MutableMapping
from enum import IntEnum as _IntEnum
from pathlib import Path
from typing import Any

import pydantic as pd
from pydantic import BaseModel as __BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field
from tcrutils.case import snake_to_camel as _snake_to_camel
from tcrutils.compare import able as _able
from tcrutils.console import console as _c
from tcrutils.types import HexInt as _HexInt
from tcrutils.types import UnixTimestampInt as _UnixTimestampInt

from ..error import add_helpful_note_to_validation_error
from .info import NPCProfileInfo, ProfileID, ProfileInfo, UserInfo

_IGNORE_KEYS: tuple[str] = ("_apiKey", "userID", "profileID")
_UPPERCASE_KEY_SUBSTRINGS: tuple[str] = ("id", "xp")

from traceback import print_exc


class _BM(__BaseModel):
	raw_json: dict = Field(default_factory=dict, exclude=True, repr=False)

	def __init__(self, **data):
		data = {k: v for k, v in data.items() if k not in _IGNORE_KEYS}
		data = {_snake_to_camel(k): v for k, v in data.items()}
		try:
			super().__init__(**data)
		except pd.ValidationError as e:
			e.raw_json = data

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
		alias_generator = lambda x: _snake_to_camel(x, always_uppercase=_UPPERCASE_KEY_SUBSTRINGS, unless_str_in_always_uppercase=True)
		"""For now let's not worry about the '_apiKey' key, ignoring it since it's useless so it's just not included in the profile object."""


if True:  # Functionality classes

	class _MEmoji:
		"""Lets pydantic models inherit `.emoji` and `.emoji`-related methods."""

		emoji: str
		"""The emoji of this object."""

		def is_emoji_unicode(self) -> bool:
			"""Whether or not the emoji of this item is a unicode emoji (aka: NOT a discord custom emoji)."""
			return not self.emoji.startswith("<")


def pickle_to_file(path: Path, o: Any) -> None:
	path.write_bytes(pickle.dumps(o))


def unpickle_from_file(path: Path) -> Any:
	return pickle.loads(path.read_bytes())
