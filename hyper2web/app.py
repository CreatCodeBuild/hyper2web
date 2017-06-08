import os

from curio import Kernel

from . import server, abstract
from .http import HTTP, Stream
from .router import Router

AbstractApp = abstract.AbstractApp
h2_server = server.h2_server


def default_get(app):
	async def f(request, response):
		route = request.stream.headers[':path'].lstrip('/')
		full_path = os.path.join(app.root, route)
		if os.path.exists(full_path):
			await response.send_file(full_path)
			# await http.send_file(stream, full_path)
		else:
			await response.send_status_code(404)
			# await http.send_error(stream, 404)
	return f


def get_index(app):
	async def f(request, response):
		await response.send_file(os.path.join(app.root, app.default_file))
		# await http.send_file(stream, os.path.join(app.root, app.default_file))
	return f


class App(AbstractApp):
	def __init__(self, address="0.0.0.0", port=5000, root='./public',
				 auto_serve_static_file=True,
				 default_file='index.html', router=Router):
		"""
		:param port: TCP port 
		:param root: root directory to serve
		:param serve_static_file: automatically serve static files without manually register routes
		:param default_file: default static file to serve 
		:param router: the router class to use
		"""
		self.port = port
		self.address = address
		self.root = os.path.abspath(root)

		# todo: implement static_file_handle and root_route
		self.default_file = default_file

		if auto_serve_static_file:
			self._router = router(default_get(self))
		else:
			self._router = router(None)

		# will server this file on GET '/'
		if default_file:
			self.get('/', get_index(self))

	def up(self):
		kernel = Kernel()
		kernel.run(h2_server(address=(self.address, self.port),
							 certfile="{}.crt.pem".format("localhost"),
							 keyfile="{}.key".format("localhost"),
							 app=self),
				   shutdown=True)

	def get(self, route: str, handler):
		self._router.register('GET', route, handler)

	def post(self, route: str, handler):
		self._router.register('POST', route, handler)

	# async
	async def handle_route(self, http: HTTP, stream: Stream):
		await self._router.handle_route(http, stream)
