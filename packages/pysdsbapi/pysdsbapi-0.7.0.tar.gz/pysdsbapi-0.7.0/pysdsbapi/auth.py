from aiohttp import ClientSession, ClientResponse, BasicAuth
from urllib.parse import urlparse

class Auth:
    """Class to make authenticated requests."""

    def __init__(self, clientSession: ClientSession, host: str, user: str, password: str):        
        """Initialize the auth."""
        
        self.clientSession = clientSession
        self.auth = BasicAuth(login=user, password=password, encoding='utf-8')
        self.host = urlparse(host)
        #If scheme is missing urlparse does not work
        if self.host.scheme is "":
            raise Exception(f"The host: {host} is invalid. Should be look like <scheme>://<hostname> or <scheme>://<hostname>:<port>")

        self.port = self.host.port if self.host.port else 3490
        self.scheme = self.host.scheme if self.host.scheme else "http"
        self.api_prefix = "api/v1"


    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""

        headers = kwargs.get("headers")
        if headers is None:
            headers = {}
        else:
            headers = dict(headers)
        
        return await self.clientSession.request(
            method, f"{self.scheme}://{self.host.hostname}:{self.port}/{self.api_prefix}/{path}", **kwargs, headers=headers, auth=self.auth,
        )