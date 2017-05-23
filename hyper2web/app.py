import os

from curio import Kernel

from . import server, abstract
from .http import HTTP, Stream
from .router import Router

AbstractApp = abstract.AbstractApp
h2_server = server.h2_server


class App(AbstractApp):
	def __init__(self, port=5000, root='./public',
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
		self.root = os.path.abspath(root)

		# todo: implement static_file_handle and root_route
		self.default_file = default_file

		if auto_serve_static_file:
			async def default_get(http, stream, parameters):
				print('default_get')
				route = stream.headers[':path'].lstrip('/')
				full_path = os.path.join(self.root, route)
				if os.path.exists(full_path):
					await http.send_file(stream, full_path)
				else:
					await http.send_error(stream, 404)

			self._router = router(default_get)
		else:
			self._router = router(None)

		# will server this file on GET '/'
		if default_file:
			async def get_index(http, stream, para):
				await http.send_file(stream, os.path.join(self.root, self.default_file))
			self.get('/', get_index)

	def up(self):
		kernel = Kernel()
		kernel.run(h2_server(address=("localhost", self.port),
							 certfile="{}.crt.pem".format("localhost"),
							 keyfile="{}.key".format("localhost"),
							 app=self))

	def get(self, route: str, handler):
		self._router.register('GET', route, handler)

	def post(self, route: str, handler):
		self._router.register('POST', route, handler)

	# async
	async def handle_route(self, http: HTTP, stream: Stream):
		await self._router.handle_route(http, stream)
