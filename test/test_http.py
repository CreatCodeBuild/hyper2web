import unittest

from hyper2web.exceptions import DifferentStreamIdException
from hyper2web.http import Stream, Request, Response
from h2.events import DataReceived


class TestStream(unittest.TestCase):

	def test_header_not_empty(self):
		"""Stream should refuse to construct if the header is Falsy or not a dict"""
		with self.assertRaises(Exception):
			Stream(stream_id=1, headers={})

	def test_raise_error_if_update_on_different_stream_id(self):
		"""A Stream should not update on an event with different stream id"""
		stream = Stream(stream_id=1, headers={'method': 'GET'})
		new_event = DataReceived()
		new_event.stream_id = 2
		new_event.data = b''
		with self.assertRaises(DifferentStreamIdException):
			stream.update(new_event)

	def test_update_on_same_stream_id_and_finalize_correctly(self):
		stream = Stream(stream_id=1, headers={'method': 'GET'})
		new_event = DataReceived()
		new_event.stream_id = 1
		new_event.data = b'some data '
		stream.update(new_event)
		stream.update(new_event)
		stream.finalize()
		self.assertEqual(b'some data some data ', stream.data)

	def test_finalize(self):
		"""Should not update a finalized Stream"""
		stream = Stream(stream_id=1, headers={'method': 'GET'})
		stream.finalize()
		with self.assertRaises(Exception):
			new_event = DataReceived()
			new_event.stream_id = 2
			new_event.data = b''
			stream.update(new_event)

class TestRequest(unittest.TestCase):
	pass

class TestResponse(unittest.TestCase):
	def test_header(self):
		res = Response(None, None)
		res.update_headers({'Some Field': 123})
		self.assertEqual(tuple(res.headers.items()), (
			(':status', '200'),
			('content-length', '0'),  # 不知用户是否应该自己计算这个
			('server', 'hyper2web'),
			('Some Field', 123)
		))


