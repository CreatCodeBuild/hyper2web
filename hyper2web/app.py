import os

from curio import Kernel

from . import server, abstract
from .http import HTTP, Stream
from .router import Router

AbstractApp = abstract.AbstractApp
h2_server = server.h2_server


def default_get(app):
	"""
	This function is the default handler for GET request whose :path is registered in the router.
	
	To be more clear, a user does not have to register GET /index.html or GET /any_static_file.xxx. Any :path which is not found in the router will initiate this method.

	This method treats all requests as a GET /static_file. If :path is not a existing file path, it returns status code 404.
	
	Users should not use this function.
	"""
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
	"""
	The default handler for GET /.
	
	The default behavior for GET / is GET /index.html.
	
	If a user specifies a default_file in the constructor of App, the behavior becomes GET /default_file
	
	Users should not use this function.
	"""
	async def f(request, response):
		await response.send_file(os.path.join(app.root, app.default_file))
		# await http.send_file(stream, os.path.join(app.root, app.default_file))
	return f


class App(AbstractApp):
	"""
	This class is the main class which users should be interact with.
	
	This is the only class which users should construct.
	"""
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
		"""
		Start the server. This is the last function users should call.
		
		Users only call this function after set up all routing handlers.
		"""
		kernel = Kernel()
		kernel.run(h2_server(address=(self.address, self.port),
							 certfile="{}.crt.pem".format("localhost"),
							 keyfile="{}.key".format("localhost"),
							 app=self),
				   shutdown=True)

	def get(self, route: str, handler):
		"""
		Register a GET handler.
		
		:param route: A string which represent a RESTful route with optional parameters
		
			.. code-block:: python
				"/path/<parameter name>/..."		
		
		:param handler: A handler function. Has to be async.
			
			.. code-block:: python
				async def handler(request, response):
					...do something...
					response.send(...)
		"""
		self._router.register('GET', route, handler)

	def post(self, route: str, handler):
		"""
		The same as self.get except that it's for POST
		"""
		self._router.register('POST', route, handler)

	# async
	async def handle_route(self, http: HTTP, stream: Stream):
		"""
		When the framework gets a incoming request, handle this request to corresponding routing handler.
		
		Only used by the framework. Users should never call it.
		"""
		await self._router.handle_route(http, stream)
