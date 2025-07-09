from dataclasses import dataclass as _dataclass

from .listed_profile import ListedProfilesClient
from .zoo import ZooClient


@_dataclass
class Client(ZooClient, ListedProfilesClient): ...
