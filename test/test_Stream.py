import unittest
from hyper2web.http import Stream
from h2.events import DataReceived

class TestStream(unittest.TestCase):

	def test_header_not_empty(self):
		stream = Stream(stream_id=1, headers={})
		assert not stream.headers

	def test_update_on_same_stream_id(self):
		stream = Stream(stream_id=1, headers={'method': 'GET'})
		new_event = DataReceived()
		new_event.stream_id = 2
		new_event.data = b''

		# should raise error
		with self.assertRaises(Exception):
			stream.update(new_event)
