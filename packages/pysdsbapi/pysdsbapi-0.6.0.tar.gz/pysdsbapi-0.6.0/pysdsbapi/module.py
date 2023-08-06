from typing import List
from .auth import Auth


class Module:
    """Class that represents a Module object in the API."""

    def __init__(self, raw_data: dict, auth: Auth):
        self.raw_data = raw_data
        self.auth = auth

    @property
    def id(self) -> str:
        """Return the id of the module."""
        return self.raw_data["id"]

    @property
    def name(self) -> str:
        """Return the name of the module."""
        return self.raw_data["name"]

    @property
    def aliases(self) -> dict:
        """Return the aliases of the module."""
        return self.raw_data["aliases"]

    @property
    def canClose(self) -> bool:
        """Return if the module is closeable."""
        return self.raw_data["canClose"]

    @property
    def source(self) -> str:
        """Return the source of the module."""
        return self.raw_data["source"]

    @property
    def state(self) -> str:
        """Return the state of the module."""
        return self.raw_data["state"]

    @property
    def targetName(self) -> str:
        """Return the targetName of the module."""
        return self.raw_data["targetName"]

    @property
    def type(self) -> str:
        """Return the type of the module."""
        return self.raw_data["type"]

    async def async_control(self, command: str):
        """Control the module."""

        response = await self.auth.request(
            "post", f"modules/command", json={"id": self.id, "command": command}
        )
        response.raise_for_status()
        #This should be made possible. Seccond update-Call necessary
        #self.raw_data = await response.json()

    async def async_update(self):
        """Update the module data."""

        response = await self.auth.request("get", f"modules/show?id={self.id}")
        response.raise_for_status()
        moduleList = await response.json()
        self.raw_data = moduleList[0]


    def __str__(self):
        return f'Module(id={self.id}, name={self.name}, state={self.state}, type={self.type})'

    def __repr__(self):
        return self.__str__()
