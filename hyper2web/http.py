"""
This module implements HTTP methods for end user

I currently think that they should be synchronized since they should not do IO
Where as endpoint module is designed for IO
"""
from collections import OrderedDict

from curio import spawn, Event, aopen

from h2 import events
from h2.connection import H2Connection

from .abstract import AbstractApp, AbstractHTTP, AbstractRequest, AbstractResponse

READ_CHUNK_SIZE = 8096


class Stream:
	"""
	As the code is right now, many stream implementation is done in endpoint.EndPointHandler
	Am moving those functionality to this class

	The current design is that application will only return complete stream to top level api
	But, since a user might also want to program on a live stream.
	For example, the client may send a giant file 1GB,
	the user will want to write this stream to disk in real time
	Also, buffering 1GB in memory is kind of stupid.

	But nonethelss, the current focus is on better organization of code instead of more API or performace.
	"""

	def __init__(self, stream_id: int, headers: dict):
		if headers and isinstance(headers, dict):
			self.stream_id = stream_id
			self.headers = headers  # as the name indicates

			# todo: 效率有待提高。也许不需要两个变量去保存数据
			# todo: 并且以后也许会有 stream programming 的需求。
			# todo: 所以一个 stream 没有结束时也可以被顶层接口用户处理
			self.buffered_data = []
			self.data = None  # I am not sure if body is just binary data, aka, bytes
		else:
			raise Exception('http.Stream: Try to construct a Stream without valid headers')

	def update(self, event: events.DataReceived):
		"""
		assume only POST stream will call this one
		"""
		if event.stream_id == self.stream_id:
			self.buffered_data.append(event.data)
		else:
			raise Exception('http.Stream: Try to update a Stream on an event with different stream id')

	def finalize(self):
		"""
		assume only POST stream will call this one
		concat all data chunks in this handler to one bytes object
		"""
		if len(self.buffered_data) > 0:
			# todo: 这里是否用 join 去处理是最好的？有待商榷。
			self.data = b''.join(self.buffered_data)
		self.buffered_data = None


class HTTP(AbstractHTTP):
	"""
	This class further implements complete HTTP2 on top of h2
	"""
	def __init__(self, app: AbstractApp, sock, connection: H2Connection):
		# not like h2 events which might only contain partial information of a request
		# a http.Stream contain full information of a request (Could pick a better name)
		# key: stream id,
		# value: all useful information of this stream (basically headers and body)
		self.streams = {}
		# stores partially completed stream only, once a stream is complete,
		# the app will create an EndPointHandler object to wrap the stream and pass it to top level API

		self.app = app
		self.sock = sock
		self.connection = connection
		self.flow_control_events = {}

	def _finalize_stream(self, stream_id):
		stream = self.streams.pop(stream_id)
		stream.finalize()
		return stream

	# async
	async def _check_event_end_stream(self, event):
		if event.stream_ended:
			stream = self._finalize_stream(event.stream_id)
			await self.app.handle_route(self, stream)

	async def handle_event(self, event: events.Event):

		if isinstance(event, events.RequestReceived):
			await spawn(self.request_received(event))

		elif isinstance(event, events.DataReceived):
			await spawn(self.data_received(event))

		elif isinstance(event, events.WindowUpdated):
			await self.window_updated(event)

		# todo: need to support all h2.events

	async def request_received(self, event: events.RequestReceived):
		"""
		Handle a request
		"""
		if event.stream_id in self.streams:
			raise Exception('RequestReceived should only be present for new stream. I assume')
		else:
			self.streams[event.stream_id] = Stream(event.stream_id, dict(event.headers))

		# I am not sure if GET will only trigger a RequestReceived event
		# this event should be METHOD independent? I should ask h2 author if all events are method independent

		# pass if this event complete a stream, create an EndPointHandler and pass it to API user
		await self._check_event_end_stream(event)

	async def data_received(self, event: events.DataReceived):
		"""
		Handle received data for a certain stream. Currently used for POST
		"""
		if event.stream_id not in self.streams:
			# But I think this situation is impossible since header should always arrive before data
			raise Exception('data before header')

		# update this handler
		self.streams[event.stream_id].update(event)
		# possibly finalize this handler
		await self._check_event_end_stream(event)

	async def wait_for_flow_control(self, stream_id):
		"""
		Blocks until the flow control window for a given stream is opened.
		"""
		evt = Event()
		self.flow_control_events[stream_id] = evt
		await evt.wait()

	async def window_updated(self, event):
		"""
		Unblock streams waiting on flow control, if needed.
		"""
		stream_id = event.stream_id

		if stream_id and stream_id in self.flow_control_events:
			evt = self.flow_control_events.pop(stream_id)
			await evt.set()
		elif not stream_id:
			# Need to keep a real list here to use only the events present at
			# this time.
			blocked_streams = list(self.flow_control_events.keys())
			for stream_id in blocked_streams:
				event = self.flow_control_events.pop(stream_id)
				await event.set()

	async def send(self, stream_id: int, headers, data: bytes=None):
		"""
		send the response to the client
		:param stream_id: the stream id associated with this request/response
		:param headers: HTTP headers. a sequence(tuple/list) of tuples
			((':status', '200'),
			 ('content-length', '0'),
			 ('server', 'hyper2web'))
		:param data: HTTP response body. Has to be bytes(binary data).
		It's users' responsibility to encode any kinds of data to binary.
		"""
		# print('HTTP.send')
		# not sure if check for None or Falsy(empty containers)
		if data is None:
			self.connection.send_headers(stream_id, headers, end_stream=True)
			await self.sock.sendall(self.connection.data_to_send())

		else:
			print('HTTP.send ', headers)

			self.connection.send_headers(stream_id, headers, end_stream=False)
			# print('HTTP.send headers')
			await self.sock.sendall(self.connection.data_to_send())
			# print('HTTP.send before body')
			# body
			i = 0
			while True:
				# print('HTTP.send in loop')
				while not self.connection.local_flow_control_window(stream_id):
					await self.wait_for_flow_control(stream_id)
				# print('HTTP.send 1')
				chunk_size = min(self.connection.local_flow_control_window(stream_id), READ_CHUNK_SIZE)
				# print('HTTP.send 2')
				# this line is sync
				data_to_send = data[i:i+chunk_size]
				end_stream = (len(data_to_send) != chunk_size)
				# print('HTTP.send 3')
				# print(stream_id, len(data_to_send), end_stream)
				try:
					self.connection.send_data(stream_id, data_to_send, end_stream=end_stream)
				except BaseException as e:
					print(e)
				# print(i, len(data_to_send), chunk_size)
				# print(data_to_send)
				# print(self.connection.data_to_send())
				await self.sock.sendall(self.connection.data_to_send())

				if end_stream:
					break
				i += chunk_size


class Request(AbstractRequest):
	def __init__(self, stream, para):
		self.stream = stream
		self.para = para


class Response(AbstractResponse):
	def __init__(self, stream_id: int, http: HTTP):
		self.stream_id = stream_id
		self.http = http
		self.headers = OrderedDict([
			(':status', '200'),
			('content-length', '0'),  # 不知用户是否应该自己计算这个
			('server', 'hyper2web')
		])

	def set_header(self, field, value):
		self.headers[field] = value

	def set_headers(self, headers):
		self.headers = headers

	def update_headers(self, headers):
		self.headers.update(headers)

	async def send_file(self, file_path):
		# 不知道这个 context manager 是否处理文件没找到
		async with aopen(file_path, mode='rb') as f:
			data = await f.read()
			self.headers['content-length'] = str(len(data))
			await self.send(data)

	async def send_status_code(self, status_code):
		self.headers[':status'] = str(status_code)
		await self.send(None)

	async def send(self, data: bytes or None):
		headers = tuple(self.headers.items())
		await self.http.send(self.stream_id, headers, data)
