import unittest

from curio import Kernel

from hyper2web.http import Stream
from hyper2web.router import Router


k = Kernel()

class TestRouter(unittest.TestCase):

	def test_raise_error_on_non_existing_route(self):
		"""If a route doesn't exist, should raise error"""
		router = Router(None, None)
		stream = Stream(1, {':path': 'x', ':method': 'GET'})

		# should raise a more specific error in the future
		with self.assertRaises(Exception):
			coroutine = router.handle_route(None, stream)
			k.run(coroutine)

	def test_get_existing_route(self):
		router = Router(None, None)
		stream = Stream(1, {':path': 'x', ':method': 'GET'})

		async def f(http, stream):
			assert http is None
			assert stream.headers[':path'] == 'x'
		router.get('x', f)
		coroutine = router.handle_route(None, stream)
		k.run(coroutine)

	def test_post_existing_route(self):
		router = Router(None, None)
		stream = Stream(1, {':path': 'x', ':method': 'POST'})

		async def f(http, stream):
			assert http is None
			assert stream.headers[':path'] == 'x'
		router.post('x', f)
		coroutine = router.handle_route(None, stream)
		k.run(coroutine)

	def test_match(self):
		# match true
		matched, parameters = Router._match('user/{userId}/name/{name}', 'user/123/name/John')
		self.assertTrue(matched)
		self.assertEqual(parameters['userId'], '123')
		self.assertEqual(parameters['name'], 'John')

		# match false
		matched, parameters = Router._match('user/{userId}/name/{name}', 'user/123/nam/John')
		self.assertFalse(matched)

	def test_parameterized_route(self):
		router = Router(None, None)
		async def f(http, stream, parameters):
			self.assertIsNone(http)
			self.assertEqual(parameters['userId'], '123')
			self.assertEqual(parameters['name'], 'John')
		router.get('user/{userId}/name/{name}', f)
		c = router.handle_route(None, Stream(1, {':path': 'user/123/name/John', ':method': 'GET'}))
		k.run(c)

	# will want to test with unicode
