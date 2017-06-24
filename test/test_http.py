import unittest
from hyper2web.http import Stream
from h2.events import DataReceived


class TestStream(unittest.TestCase):

	def test_header_not_empty(self):
		"""Stream should refuse to construct if the header is Falsy or not a dict"""
		with self.assertRaises(Exception):
			Stream(stream_id=1, headers={})

	def test_update_on_same_stream_id(self):
		"""A Stream should not update on an event with different stream id"""
		stream = Stream(stream_id=1, headers={'method': 'GET'})
		new_event = DataReceived()
		new_event.stream_id = 2
		new_event.data = b''
		with self.assertRaises(Exception):
			stream.update(new_event)

	def test_finalize(self):
		"""Should not update a finalized Stream"""
		stream = Stream(stream_id=1, headers={'method': 'GET'})
		stream.finalize()
		with self.assertRaises(Exception):
			new_event = DataReceived()
			new_event.stream_id = 2
			new_event.data = b''
			stream.update(new_event)
