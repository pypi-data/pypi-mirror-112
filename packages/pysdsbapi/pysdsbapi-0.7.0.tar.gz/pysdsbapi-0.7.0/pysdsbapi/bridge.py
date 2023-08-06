from typing import List
from .auth import Auth


class Bridge:
    """Class that represents a Blum Bridge object in the API."""

    def __init__(self, raw_data: dict, auth: Auth):
        self.raw_data = raw_data
        self.auth = auth


    @property
    def bridgeId(self) -> str:
        """Return the id of the bridge."""
        return self.raw_data["bridgeId"]

    @property
    def bridgeAppVersion(self) -> str:
        """Return the bridgeAppVersion of the bridge."""
        return self.raw_data["bridgeAppVersion"]
    
    @property
    def dps(self) -> str:
        """Return the dps of the bridge."""
        return self.raw_data["dps"]

    @property
    def iothub(self) -> str:
        """Return the iothub of the bridge."""
        return self.raw_data["iothub"]
    
    @property
    def rfVersion(self) -> str:
        """Return the rfVersion of the bridge."""
        return self.raw_data["rfVersion"]


    def __str__(self):
        return f'Bridge(bridgeId={self.bridgeId}, bridgeAppVersion={self.bridgeAppVersion}, dps={self.dps}, iothub={self.iothub}, rfVersion={self.rfVersion})'

    def __repr__(self):
        return self.__str__()