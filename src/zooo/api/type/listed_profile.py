from ._base import _BM, NPCProfileInfo, ProfileInfo, _HexInt, _MEmoji, pd


class _ListedProfileIcon(_BM, _MEmoji):
	"""Represents this profile's icon in two different formats - emoji and HTML."""

	emoji: str
	"""This profile's icon as a unicode emoji."""
	parsed: str
	"""This profile's icon as an HTML `<img>`."""


class ListedProfile(_BM):
	"""Represents one element of list acquired from '/api/profiles' endpoint. Not to be confused with `Zoo`."""

	id: ProfileInfo
	"""ProfileInfo (Full ID) of this profile, for example `'507642999992352779_kitsune'`."""
	name: str
	"""Zoo name of this profile."""
	color: _HexInt
	"""Embed color of this profile. Unlike `Zoo.color` this field is always a valid color, if it's unset it's just 0x000000 (in `Zoo.color` it may be None)."""
	private: bool
	"""Whether this profile is private or not."""
	viewable: bool
	"""Whether with the current auth you can access this profile's Zoo via `/api/profile` (`client.fetch_zoo()`)."""
	current: bool
	"""Whether this profile is the current profile."""
	score: int
	"""Zoo score of this profile."""
	icon: _ListedProfileIcon
	"""Represents this profile's icon in two different formats - emoji and HTML."""

	@pd.field_validator("id", mode="before")
	@classmethod
	def _v_id(cls, v):
		return ProfileInfo.from_str(v)

	@pd.field_validator("color", mode="before")
	@classmethod
	def _v_color(cls, v):
		if v is None:
			return None
		return _HexInt(v)

	@pd.field_validator("viewable", mode="before")
	@classmethod
	def _v_viewable(cls, v):
		return bool(v)

	@property
	def is_npc(self):
		return isinstance(self.id, NPCProfileInfo)

	def __hash__(self):
		"""Generate a hash based on the unique `id`."""
		return hash(self.id)

	def __eq__(self, other):
		"""Determine equality based on the unique `id`."""
		if isinstance(other, ListedProfile):
			return self.id == other.id
		return False
