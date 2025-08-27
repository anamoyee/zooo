import profile
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from aiohttp.helpers import validate_etag_value


class ProfileID(StrEnum):
	"""The `"_fox"`, `"_cat"` part of a whole ProfileInfo."""

	ROBO = "robo"
	KITSUNE = "kitsune"

	if True:  # NPCs.
		ROBOTURT = "roboturt"
		MURPHY = "murphy"
		KRYPTO = "krypto"
		JAXPER = "jaxper"
		OTTO = "otto"

	if True:  # Common Animals
		OX = "ox"
		DOG = "dog"
		FLY = "fly"
		PIG = "pig"
		CAT = "cat"
		BAT = "bat"
		COW = "cow"
		FOX = "fox"
		DUCK = "duck"
		CRAB = "crab"
		FISH = "fish"
		FROG = "frog"
		BEAR = "bear"
		DOVE = "dove"
		WORM = "worm"
		SEAL = "seal"
		DEER = "deer"
		MOUSE = "mouse"
		SLOTH = "sloth"
		HIPPO = "hippo"
		SHEEP = "sheep"
		SKUNK = "skunk"
		SQUID = "squid"
		SNAIL = "snail"
		KOALA = "koala"
		CHICK = "chick"
		WHALE = "whale"
		ZEBRA = "zebra"
		HORSE = "horse"
		CAMEL = "camel"
		RABBIT = "rabbit"
		LIZARD = "lizard"
		BEAVER = "beaver"
		PARROT = "parrot"
		SPIDER = "spider"
		SHRIMP = "shrimp"
		BEETLE = "beetle"
		TURKEY = "turkey"
		GORILLA = "gorilla"
		LEOPARD = "leopard"
		PENGUIN = "penguin"
		CHICKEN = "chicken"
		GIRAFFE = "giraffe"
		SNOWMAN = "snowman"
		HAMSTER = "hamster"
		CRICKET = "cricket"
		ELEPHANT = "elephant"
		DINOSAUR = "dinosaur"
		HEDGEHOG = "hedgehog"
		CROCODILE = "crocodile"
		CATERPILLAR = "caterpillar"

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		from tcrutils.print import FMT_BRACKETS, FMTC

		return f"{FMTC.TYPE if syntax_highlighting else ''}{self.__class__.__name__}{FMTC._ if syntax_highlighting else ''}" + FMT_BRACKETS[tuple][syntax_highlighting] % fmt_iterable(str(self))


@dataclass(frozen=True)
class UserInfo:
	"""Identification info for a given user, but not a specific profile."""

	discord_id: int

	def __str__(self):
		return f"{self.discord_id}"

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		from tcrutils.print import FMT_BRACKETS

		return fmt_iterable(self.__class__) + FMT_BRACKETS[tuple][syntax_highlighting] % fmt_iterable(self.discord_id)

	@classmethod
	def from_str(cls, s: str, /) -> Self:
		if not s.isdigit():
			raise ValueError("Invalid user info string: invalid discord id")

		return cls(int(s))


@dataclass(kw_only=True, frozen=True)
class ProfileInfo:
	"""Identification info for a specific profile of a given user."""

	user: UserInfo
	profile_id: ProfileID

	@classmethod
	def from_parts(cls, *, discord_id: int, profile_id: ProfileID) -> Self:
		return cls(user=UserInfo(discord_id), profile_id=profile_id)

	@classmethod
	def from_str(cls, s: str, /) -> Self:
		"""Try to create a ProfileInfo from a string, if not able, raise ValueError."""

		if not s.count("_") == 1:
			raise ValueError("Invalid profile info string: invalid number of `'_'` characters")

		discord_id_str, profile_id_str = s.split("_")

		user = UserInfo.from_str(discord_id_str)

		profile_id = ProfileID(profile_id_str)

		return cls(user=user, profile_id=profile_id)

	def __str__(self):
		return f"{self.user}_{self.profile_id}"

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		from tcrutils.print import FMT_BRACKETS

		return fmt_iterable(self.__class__) + FMT_BRACKETS[tuple][syntax_highlighting] % fmt_iterable(str(self))


class NPCProfileInfo(StrEnum):
	ROBOTURT = "roboturt"
	MURPHY = "murphy"
	KRYPTO = "krypto"
	JAXPER = "jaxper"
	OTTO = "otto"

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		from tcrutils.print import FMT_BRACKETS, FMTC

		return f"{FMTC.TYPE if syntax_highlighting else ''}{self.__class__.__name__}{FMTC._ if syntax_highlighting else ''}" + FMT_BRACKETS[tuple][syntax_highlighting] % fmt_iterable(str(self))

	@classmethod
	def from_str(cls, s: str, /):
		"""Try to create an NPCProfileInfo from a string, if not able, raise ValueError."""
		return cls(s)  # raises ValueError
