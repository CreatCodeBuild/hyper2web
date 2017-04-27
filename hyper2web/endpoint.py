"""
This module is not working yet. Need Improvement.
"""
import mimetypes
import os

# from hyper2web import http

# The maximum amount of a file we'll send in a single DATA frame.
READ_CHUNK_SIZE = 8192

class EndPointHandler:
	def __init__(self, server, sock, connection, stream):
		self.server = server
		self.socket = sock
		self.connection = connection
		#
		self.stream = stream

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

		self.connection.send_headers(self.stream.stream_id, response_headers)
		await self.socket.sendall(self.connection.data_to_send())

		# Body
		self.connection.send_data(self.stream.stream_id, bytes(data), end_stream=True)
		await self.socket.sendall(self.connection.data_to_send())

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

		self.connection.send_headers(self.stream.stream_id, response_headers)
		await self.socket.sendall(self.connection.data_to_send())

		with open(file_path, 'rb', buffering=0) as fileobj:
			while True:
				while not self.connection.local_flow_control_window(self.stream.stream_id):
					await self.server.wait_for_flow_control(self.stream.stream_id)

				chunk_size = min(
					self.connection.local_flow_control_window(self.stream.stream_id),
					READ_CHUNK_SIZE,
				)

				# this line is sync
				data = fileobj.read(chunk_size)
				keep_reading = (len(data) == chunk_size)

				self.connection.send_data(self.stream.stream_id, data, not keep_reading)
				await self.socket.sendall(self.connection.data_to_send())

				if not keep_reading:
					break

	async def send_error(self, error):
		response_headers = (
			(':status', str(error)),
			('content-length', '0'),
			('server', 'curio-h2'),
		)
		self.connection.send_headers(self.stream.stream_id, response_headers, end_stream=True)
		await self.socket.sendall(self.connection.data_to_send())
