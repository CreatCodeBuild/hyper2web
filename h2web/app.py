import os

from curio import Kernel

from h2web.curio_server import h2_server



# todo: move routing functionality from curio_server to app
# todo: implement static_file_handle and root_route
class App:
	def __init__(self, port=5000, root='./public', static_file_handle='auto', root_route='index.html'):
		self.port = port
		self.root = os.path.abspath(root)
		print(self.root)
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
							 app=self))

	def register_route(self, method: str, route: str, handler):
		assert method in ['GET', 'POST']
		self.routes[method][route] = handler

	def get(self, route: str, handler=None):
		self.register_route('GET', route, handler)
