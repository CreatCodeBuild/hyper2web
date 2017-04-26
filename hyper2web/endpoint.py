"""
This module is not working yet. Need Improvement.
"""
import mimetypes
import os
import h2.events

# The maximum amount of a file we'll send in a single DATA frame.
READ_CHUNK_SIZE = 8192

active_end_points = {}  # stream_id: end_point_handler

class EndPointHandler:
	def __init__(self, server, sock, connection, stream_id, header, route):
		self.server = server
		self.socket = sock
		self.connection = connection
		#
		self.stream_id = stream_id
		self.header = header
		self.route = route
		#
		self.buffered_data = []
		self.data = None

	def update(self, event: h2.events.DataReceived):
		"""
		assume only POST stream will call this one
		"""
		self.buffered_data.append(event.data)

	def finalize(self):
		"""
		assume only POST stream will call this one
		concat all data chunks in this handler to one bytes object
		"""
		self.data = b''.join(self.buffered_data)
		self.buffered_data = None

	"""async functions"""
	async def send_and_end(self, data):

		# Header
		content_type, content_encoding = mimetypes.guess_type(data)
		data = bytes(data, encoding='utf8')
		response_headers = [
			(':status', '200'),
			('content-length', str(len(data))),
			('server', 'hyper2web'),
		]
		if content_type:
			response_headers.append(('content-type', content_type))
		if content_encoding:
			response_headers.append(('content-encoding', content_encoding))

		self.connection.send_headers(self.stream_id, response_headers)
		await self.socket.sendall(self.connection.data_to_send())

		# Body
		self.connection.send_data(self.stream_id, bytes(data), end_stream=True)
		await self.socket.sendall(self.connection.data_to_send())

	# todo: implement it
	async def send_file(self, file_path):
		"""
		Send a file, obeying HTTP/2 flow control rules
		"""
		# use Python default open
		filesize = os.stat(file_path).st_size
		content_type, content_encoding = mimetypes.guess_type(file_path)
		response_headers = [
			(':status', '200'),
			('content-length', str(filesize)),
			('server', 'curio-h2'),
		]
		if content_type:
			response_headers.append(('content-type', content_type))
		if content_encoding:
			response_headers.append(('content-encoding', content_encoding))

		self.connection.send_headers(self.stream_id, response_headers)
		await self.socket.sendall(self.connection.data_to_send())

		with open(file_path, 'rb', buffering=0) as fileobj:
			while True:
				while not self.connection.local_flow_control_window(self.stream_id):
					await self.server.wait_for_flow_control(self.stream_id)

				chunk_size = min(
					self.connection.local_flow_control_window(self.stream_id),
					READ_CHUNK_SIZE,
				)

				# this line is sync
				data = fileobj.read(chunk_size)
				keep_reading = (len(data) == chunk_size)

				self.connection.send_data(self.stream_id, data, not keep_reading)
				await self.socket.sendall(self.connection.data_to_send())

				if not keep_reading:
					break

	async def send_error(self, error):
		response_headers = (
			(':status', str(error)),
			('content-length', '0'),
			('server', 'curio-h2'),
		)
		self.connection.send_headers(self.stream_id, response_headers, end_stream=True)
		await self.socket.sendall(self.connection.data_to_send())
