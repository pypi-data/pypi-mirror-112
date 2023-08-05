from aiohttp import ClientSession, ClientResponse, BasicAuth



class Auth:
    """Class to make authenticated requests."""


    def __init__(self, clientSession: ClientSession, host: str, user: str, password: str, port=3490, api_prefix="api/v1",):        
        """Initialize the auth."""        
        self.clientSession = clientSession        
        self.host = host
        self.auth = BasicAuth(login=user, password=password, encoding='utf-8')
        self.port = port
        self.api_prefix = api_prefix


    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:        
        """Make a request."""        
        headers = kwargs.get("headers")
        if headers is None:            
            headers = {}        
        else:            
            headers = dict(headers)
        

        return await self.clientSession.request(
            method, f"{self.host}:{self.port}/{self.api_prefix}/{path}", **kwargs, headers=headers, auth=self.auth,        
        )