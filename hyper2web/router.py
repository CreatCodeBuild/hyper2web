import os

from .abstract import AbstractRouter
from .http import HTTP, Stream


class Router(AbstractRouter):
	"""User should never construct Router"""

	def __init__(self, default_get, default_post):
		self._routes = {
			'GET': {},
			'POST': {}
		}
		self.method_default = {
			'GET': default_get,
			'POST': default_post
		}

	def _route(self, method: str, route: str, handler):
		assert method in ['GET', 'POST']
		self._routes[method][route] = handler

	def get(self, route: str, handler):
		self._route('GET', route, handler)

	def post(self, route: str, handler):
		self._route('POST', route, handler)

	# async
	async def handle_route(self, http: HTTP, stream: Stream):
		print('app.App.handle_route')

		route = stream.headers[':path'].lstrip('/')
		method = stream.headers[':method']

		handler = self._routes[method].get(route, self.method_default[method])
		await handler(http, stream)
