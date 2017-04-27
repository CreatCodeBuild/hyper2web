import os
import sys
sys.path.append(os.path.abspath('..'))
from hyper2web import app, endpoint
from hyper import HTTPConnection
from multiprocessing import Process

import unittest


"""
Try to use Dependency Injection to test EndPointHandler

First, I need to make up a class that has the same interface as H2Server
"""

class FakeServer:
	async def wait_for_flow_control(self, stream_id):
		await

class TestEndPointHandler(unittest.TestCase):

	# def setUp(self):
	# 	if __name__ == '__main__':
	# 		p = Process(target=set_up_server)
	# 		p.start()

	def test_response(self):
		conn = HTTPConnection('localhost:5000')
		conn.request('GET', 'test_get')
		resp = conn.get_response()

		self.assertEqual(resp.read(), 'test_get')


if __name__ == '__main__':
	unittest.main()


