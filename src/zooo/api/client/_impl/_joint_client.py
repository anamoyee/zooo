from ._lp import _LPClientMixin
from ._settings import _SettingsClientMixin
from ._zoo import _ZooClientMixin


class Client(_ZooClientMixin, _LPClientMixin, _SettingsClientMixin):
	pass
