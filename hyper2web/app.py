import os

from curio import Kernel

from . import server, abstract
from .http import HTTP, Stream

AbstractApp = abstract.AbstractApp
h2_server = server.h2_server


class App(AbstractApp):
	def __init__(self, port=5000, root='./public', static_file_handle='auto', root_route='index.html'):
		self.port = port
		self.root = os.path.abspath(root)
		self.routes = {'GET': {}, 'POST': {}}

		# todo: implement static_file_handle and root_route
		self.static_file_handle = static_file_handle
		self.root_route = root_route

	def up(self):
		kernel = Kernel()
		kernel.run(h2_server(address=("localhost", self.port),
							 certfile="{}.crt.pem".format("localhost"),
							 keyfile="{}.key".format("localhost"),
							 app=self),
				   shutdown=True)

	def register_route(self, method: str, route: str, handler):
		assert method in ['GET', 'POST']
		self.routes[method][route] = handler

	def get(self, route: str, handler):
		self.register_route('GET', route, handler)

	def post(self, route: str, handler):
		self.register_route('POST', route, handler)

	# async
	async def handle_route(self, http: HTTP, stream: Stream):
		print('app.App.handle_route')
    
		route = stream.headers[':path'].lstrip('/')
		if route in self.routes['GET'] or route in self.routes['POST']:
			await self.routes[stream.headers[':method']][route](http, stream)
		else:
			# if route is not registered, assume it is requesting files
			full_path = os.path.join(self.root, route)
			if os.path.exists(full_path):
				await http.send_file(stream, full_path)
			else:
				await http.send_error(stream, 404)
