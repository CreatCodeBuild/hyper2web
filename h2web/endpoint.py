"""
This module is not working yet. Need Improvement.
"""


import os


class EndPointHandler:
	def __init__(self, sock, connection: h2.connection.H2Connection, header, stream_id):
		self.socket = sock
		self.connection = connection
		self.header = header
		self.stream_id = stream_id

	async def send_and_end(self, data):

		# Header
		content_type, content_encoding = mimetypes.guess_type(data)
		data = bytes(data, encoding='utf8')
		response_headers = [
			(':status', '200'),
			('content-length', str(len(data))),
			('server', 'curio-h2'),
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

	async def send_file(self, file_path, stream_id):
		"""
		Send a file, obeying the rules of HTTP/2 flow control.
		"""
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

		self.connection.send_headers(stream_id, response_headers)
		await self.socket.sendall(self.connection.data_to_send())

		with open(file_path, 'rb', buffering=0) as f:
			await self._send_file_data(f, stream_id)

	async def _send_file_data(self, fileobj, stream_id):
		"""
		Send the data portion of a file. Handles flow control rules.
		"""
		while True:
			while not self.conn.local_flow_control_window(stream_id):
				await self.wait_for_flow_control(stream_id)

			chunk_size = min(
				self.conn.local_flow_control_window(stream_id),
				READ_CHUNK_SIZE,
			)

			data = fileobj.read(chunk_size)
			keep_reading = (len(data) == chunk_size)

			self.conn.send_data(stream_id, data, not keep_reading)
			await self.sock.sendall(self.conn.data_to_send())

			if not keep_reading:
				break