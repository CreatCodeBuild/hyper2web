import os

from .abstract import AbstractRouter
from .http import HTTP, Stream


class Router(AbstractRouter):
	"""User should never construct Router"""

	# todo: I may want to change the constructor
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

	def match(self, path: str):
		"""
		'user/{userId}' should match 'user/abc'
		userId = abc
		return a tuple (matched, parameters)
		matched is the route which matches the incoming path
		parameters is a dict of parameters and their values
		"""
		# todo: now the problem is how to implement it
		# todo: pattern matching should be independent from :method,
		# todo: but the current implementation doesn't support it. Should improve it later.
		# GET
		for route in self._routes['GET'].keys():
			matched, parameters = self._match(route, path)
			if matched:
				return route, parameters

		# POST
		pass

	@classmethod
	def _match(cls, route, path):
		# todo: it seems like that regular expression is not necessary
		route = route.split('/')
		path = path.split('/')
		if len(route) != len(path):
			return False, None
		else:
			# todo: implement it
			parameters = {}
			for r, p in zip(route, path):
				if r[0] == '{' and r[-1] == '}':
					parameters[r[1:-1]] = p
				elif r != p:
					return False, None
			return True, parameters

	# async
	async def handle_route(self, http: HTTP, stream: Stream):
		print('app.App.handle_route')

		route = stream.headers[':path'].lstrip('/')
		method = stream.headers[':method']

		handler = self._routes[method].get(route, self.method_default[method])
		await handler(http, stream)
