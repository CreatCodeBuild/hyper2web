import unittest

from curio import Kernel

from hyper2web.http import Stream
from hyper2web.router import Router


class TestRouter(unittest.TestCase):

	def setUp(self):
		self.k = Kernel()

	def tearDown(self):
		async def f():
			return
		self.k.run(f, shutdown=True)

	def test_raise_error_on_non_existing_route(self):
		"""If a route doesn't exist, should raise error"""
		router = Router(None)
		stream = Stream(1, {':path': 'x', ':method': 'GET'})

		# should raise a more specific error in the future
		with self.assertRaises(Exception):
			coroutine = router.handle_route(None, stream)
			self.run(coroutine)

	def test_get_existing_route(self):
		router = Router(None)

		async def f(req, res):
			assert req.stream.headers[':path'] == 'x'
			assert res.http is None
		router.register('GET', route='x', handler=f)

		stream = Stream(1, {':path': 'x', ':method': 'GET'})
		coroutine = router.handle_route(None, stream)
		self.k.run(coroutine)

	def test_post_existing_route(self):
		router = Router(None)

		async def f(req, res):
			assert res.http is None
			assert req.stream.headers[':path'] == 'x'
		router.register('POST', route='x', handler=f)

		stream = Stream(1, {':path': 'x', ':method': 'POST'})
		coroutine = router.handle_route(None, stream)

		self.k.run(coroutine)

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
		router = Router(None)
		async def f(req, res):
			self.assertIsNone(res.http)
			self.assertEqual(req.para['userId'], '123')
			self.assertEqual(req.para['name'], 'John')
		router.register('GET', route='user/{userId}/name/{name}', handler=f)

		stream = Stream(1, {':path': 'user/123/name/John', ':method': 'GET'})
		c = router.handle_route(None, stream)
		self.k.run(c)

	# will want to test with unicode
