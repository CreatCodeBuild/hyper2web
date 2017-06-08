"""
Define All Abstract Types in this module
Mainly for Better Organization of Code and For Better IDE Type Inferences
"""


class AbstractApp:
    def up(self):
        raise NotImplementedError

    def get(self, route: str, handler):
        raise NotImplementedError

    def post(self, route: str, handler):
        raise NotImplementedError

    async def handle_route(self, http, stream):
        raise NotImplementedError


class AbstractRouter:
    def register(self, method: str, route: str, handler):
        raise NotImplementedError

    async def handle_route(self, http, stream):
        raise NotImplementedError


class AbstractHTTP:
    async def handle_event(self, event):
        raise NotImplementedError

    async def send_and_end(self, stream, data):
        raise NotImplementedError

    async def send_file(self, stream, file_path):
        raise NotImplementedError

    async def send_error(self, stream, error):
        raise NotImplementedError

    async def send(self, stream_id, headers, data):
        raise NotImplementedError


class AbstractResponse:
    """
    A Response should be constructed by the router.
    The router passes Stream information such as stream id to the Response object
    and Response object is passed to the end point function for top level users' use.
    
    The flow control is handled by the HTTP class. Therefore, a send method always ends the response.
    
    All send methods should call HTTP's send method
    """
    def __init__(self, stream_id: int, http: AbstractHTTP):
        self.stream_id = stream_id
        self.http = http
        self.headers = {
            ':status': '200',
            'content-length': '0',  # 不知用户是否应该自己计算这个
            'server': 'hyper2web'
        }

    async def send(self, data: bytes):
        """
        send this response.
        :param headers: HTTP headers
        :param data: Body of the response. Has to be bytes
        That means, if you want to send some string, you have to convert the string to bytes.
        The framework does not do type conversion for you. It just fails if incorrect type is passed.
        """
        raise NotImplementedError

    async def send_file(self, file_path):
        raise NotImplementedError

    async def send_status_code(self, status_code):
        raise NotImplementedError


class AbstractRequest:
    pass
