import os

from curio import Kernel

from hyper2web.server import h2_server


# todo: move routing functionality from curio_server to app
# todo: implement static_file_handle and root_route
class App:
	def __init__(self, port=5000, root='./public', static_file_handle='auto', root_route='index.html'):
		self.port = port
		self.root = os.path.abspath(root)
		self.server = None
		self.routes = {'GET': {}, 'POST': {}}
		self.static_file_handle = static_file_handle
		self.root_route = root_route

	def up(self):
		kernel = Kernel()
		print("Try GETting:")
		print("   (Accept all the warnings)")
		kernel.run(h2_server(address=("localhost", self.port),
							 root=self.root,
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
		if endpoint.route in self.routes['GET'] or endpoint.route in self.routes['POST']:
			await self.routes[endpoint.header[':method']][endpoint.route](endpoint)
		else:
			# if route is not registered, assume it is requesting files
			full_path = os.path.join(self.root, endpoint.route)
			if os.path.exists(full_path):
				await endpoint.send_file(full_path)
			else:
				await endpoint.send_error(404)
