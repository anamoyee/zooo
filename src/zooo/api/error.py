from dataclasses import dataclass as _dataclass

from .._version import __version__


def error_from_data(data: dict) -> "None | Error":
	"""If passed in data contains an error, return that error, otherwise return None."""
	if not isinstance(data, dict):
		return None

	if not (data.get("apiError") or data.get("error") or data.get("invalid")):
		return None

	err_type = data.get("error", "")

	if err_type not in PROFILE_ERROR_MAPPING:
		err_type = None

	return PROFILE_ERROR_MAPPING[err_type](
		raw_json=data,
		name=data.get("name", ""),
		msg=data.get("msg", ""),
		type=err_type,
	)


def raise_from_data(data: dict) -> None:
	"""If passed in data contains an error, raise that error, otherwise return None."""
	if err := error_from_data(data):
		raise err


####################
### Base Classes ###
####################


@_dataclass(kw_only=True)
class Error(Exception):
	"""Base class for all `zooo` errors."""

	raw_json: dict

	def __str__(self) -> str:
		return str(self.raw_json)

	def __tcr_fmt__(self=None, *, fmt_iterable, syntax_highlighting, **kwargs):
		if self is None:
			raise NotImplementedError

		from tcrutils.print import FMT_ASTERISK, FMT_BRACKETS

		field_names = {k for k in self.__dataclass_fields__ if k != "raw_json"}

		field_items = {k: getattr(self, k) for k in field_names}

		return fmt_iterable(self.__class__) + FMT_BRACKETS[tuple][syntax_highlighting] % (FMT_ASTERISK[syntax_highlighting] + fmt_iterable(field_items))


@_dataclass
class InternalError(Error):
	"""Colon's servers reported an internal error."""

	name: str
	msg: str

	def __str__(self) -> str:
		return f"{self.name}: {self.msg}"


@_dataclass(kw_only=True)
class ZooMsgError(Error):
	"""Base class for all Zoo & Profiles errors, except the InternalError which does not follow the spec."""

	name: str
	msg: str
	type: str

	def __str__(self) -> str:
		return f"{self.name}: {self.msg} (type={self.type!r})"


# Zoo


class ZooError(ZooMsgError):
	"""Base class for all `/api/profile` endpoint errors."""


class ZooDisabledError(ZooError):
	"""Requesqted profile's info is unavailable because it has been disabled by Colon."""


class ZooNotFoundError(ZooError):
	"""Requested profile doesn't seem to exist."""


class ZooPrivateError(ZooError):
	"""Requested profile is set to private by its owner and cannot be publicly viewed."""


class ZooCursedError(ZooError):
	"""Requested profile is under a 💀 Curse of Invisibility."""


PROFILE_ERROR_MAPPING = {
	None: ZooError,
	"profileDisabled": ZooDisabledError,
	"private": ZooPrivateError,
	"invisible": ZooCursedError,
	"notFound": ZooNotFoundError,
}

# ListedProfile


class ListedProfileError(ZooMsgError):
	"""Base class for all `/api/profiles` endpoint errors."""


class ListedProfileNotFoundError(ListedProfileError):
	"""Requested user doesnt seem to have any profiles."""


####################
### Helper Stuff ###
####################


def add_helpful_note_to_validation_error(e: BaseException):
	import sys

	if sys.excepthook is sys.__excepthook__:
		color_red = "\x1b[1;31m"
		color_green = "\x1b[1;32m"
		color_reset = "\x1b[0m"
	else:
		color_red = ""
		color_green = ""
		color_reset = ""

	from sys import executable

	e.add_note(
		f"""

{color_red}\
pydantic.ValidationError - HOW TO FIX
	The above error may be caused by an outdated zoo version (current version: {__version__})
	Please update with (run this in your terminal/cmd):
		{color_green}{executable} -m pip install --upgrade zooo{color_red}
	If there are no new versions (you noticed it did not update) you can try running the command later
	If the issue persists DM me on discord @anamoyee and tell me zooo broke again.{color_reset}
"""[1:-1]
	)
