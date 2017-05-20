import unittest

from curio import run

from hyper2web.http import Stream
from hyper2web.router import Router


class TestRouter(unittest.TestCase):

	def test_handle_existing_route_only(self):
		"""If a route doesn't exist, should raise error"""
		router = Router(None, None)
		stream = Stream(1, {':path': 'x', ':method': 'GET'})

		# should raise a more specific error in the future
		with self.assertRaises(Exception):
			coroutine = router.handle_route(None, stream)
			run(coroutine)

	# todo: this test has some problem
	def test_get_existing_route(self):
		router = Router(None, None)
		stream = Stream(1, {':path': 'x', ':method': 'GET'})

		async def f(http, stream):
			assert http is None
			assert stream.headers[':path'] == 'x'
		router.get('x', f)
		coroutine = router.handle_route(None, stream)
		run(coroutine)

	def test_post_existing_route(self):
		router = Router(None, None)
		stream = Stream(1, {':path': 'x', ':method': 'POST'})

		async def f(http, stream):
			assert http is None
			assert stream.headers[':path'] == 'x'
		router.post('x', f)
		coroutine = router.handle_route(None, stream)
		run(coroutine)

	def test_match(self):
		# match true
		matched, parameters = Router._match('user/{userId}/name/{name}', 'user/123/name/John')
		self.assertTrue(matched)
		self.assertEqual(parameters['userId'], '123')
		self.assertEqual(parameters['name'], 'John')

		# match false
		matched, parameters = Router._match('user/{userId}/name/{name}', 'user/123/nam/John')
		self.assertFalse(matched)

	# will want to test with unicode
