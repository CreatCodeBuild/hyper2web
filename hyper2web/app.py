import os

from curio import Kernel

from hyper2web import server, abstract

AbstractApp = abstract.AbstractApp
h2_server = server.h2_server


# todo: move routing functionality from curio_server to app
# todo: implement static_file_handle and root_route
class App(AbstractApp):
	def __init__(self, port=5000, root='./public', static_file_handle='auto', root_route='index.html'):
		self.port = port
		self.root = os.path.abspath(root)
		self.routes = {'GET': {}, 'POST': {}}
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

	async def handle_route(self, endpoint):
		print('app.handle_route')
		print(type(endpoint))
		print(endpoint.stream)
		print(endpoint.stream.headers)
		route = endpoint.stream.headers[':path'].lstrip('/')
		print('route')
		if route in self.routes['GET'] or route in self.routes['POST']:
			await self.routes[endpoint.stream.headers[':method']][route](endpoint)
		else:
			print('123')
			# if route is not registered, assume it is requesting files

			full_path = os.path.join(self.root, route)
			if os.path.exists(full_path):
				await endpoint.send_file(full_path)
			else:
				await endpoint.send_error(404)
