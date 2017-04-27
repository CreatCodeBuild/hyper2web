"""
This module implements HTTP methods for end user

I currently think that they should be synchronized since they should not do IO
Where as endpoint module is designed for IO
"""

from curio import spawn, Event

from h2 import events

from .endpoint import EndPointHandler
from .abstract import AbstractApp
# from hyper2web.server import H2Server

class HTTP:
	"""
	This class further implements complete HTTP2 on top of h2
	"""
	def __init__(self, app: AbstractApp, server):
		# not like h2 events which might only contain partial information of a request
		# a http.Stream contain full information of a request (Could pick a better name)
		# key: stream id,
		# value: all useful information of this stream (basically headers and body)
		self.streams = {}
		# stores partially completed stream only, once a stream is complete,
		# the app will create an EndPointHandler object to wrap the stream and pass it to top level API

		self.app = app
		self.server = server
		self.flow_control_events = {}

	async def handle_event(self, event: events.Event):

		if isinstance(event, events.RequestReceived):
			print(1)
			await spawn(self.request_received(event))

		elif isinstance(event, events.DataReceived):
			print(2)
			await spawn(self.data_received(event))

		elif isinstance(event, events.WindowUpdated):
			print(3)
			await self.window_updated(event)

		# todo: need to support all h2.events

	async def request_received(self, event: events.RequestReceived):
		"""
		Handle a request
		"""
		# endpoint_handler = EndPointHandler(self, self.sock, self.conn, stream_id=stream_id, header=headers, route=route)
		if event.stream_id in self.streams:
			raise Exception('RequestReceived should only be present for new stream. I assume')
		else:
			print('xxx')
			self.streams[event.stream_id] = Stream(event.stream_id, dict(event.headers))

		# I am not sure if GET will only trigger a RequestReceived event
		# this event should be METHOD independent? I should ask h2 author if all events are method independent

		# pass if this event complete a stream, create an EndPointHandler and pass it to API user
		if event.stream_ended:
			stream = self.streams.pop(event.stream_id)
			print(stream)
			await self.app.handle_route(
				EndPointHandler(
					server=self.server,
					sock=self.server.sock,
					connection=self.server.conn,
					stream=stream))

	async def data_received(self, event: events.DataReceived):
		"""
		Handle received data for a certain stream. Currently used for POST
		"""
		if event.stream_id not in self.streams:
			# But I think this situation is impossible since header should always arrive before data
			print('data before header')
			raise Exception('data before header')


		# update this handler
		self.streams[event.stream_id].update(event)
		# possibly finalize this handler
		if event.stream_ended:
			stream = self.streams.pop(event.stream_id)
			print(stream)
			stream.finalize()
			await self.app.handle_route(
				EndPointHandler(
					server=self.server,
					sock=self.server.sock,
					connection=self.server.conn,
					stream=stream))

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
		return

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

			self.buffered_data = []
			self.data = None   # I am not sure if body is just binary data, aka, bytes
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
			self.data = b''.join(self.buffered_data)
		self.buffered_data = None

class GET:
	pass

class POST:
	pass

class PUT:
	pass

class DELETE:
	pass

class PATCH:
	pass
