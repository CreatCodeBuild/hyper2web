"""
Define All Abstract Types in this module
Mainly for Better Organization of Code and For Better IDE Type Inferences
"""

class AbstractApp:
    def up(self):
        raise NotImplementedError

    def register_route(self, method: str, route: str, handler):
        raise NotImplementedError

    def get(self, route: str, handler):
        raise NotImplementedError

    def post(self, route: str, handler):
        raise NotImplementedError

    async def handle_route(self, endpoint):
        raise NotImplementedError
