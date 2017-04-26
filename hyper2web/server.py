#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
server.py
~~~~~~~~~~~~~~~

A fully-functional HTTP/2 server written for curio.

Requires Python 3.5+.
"""
import os
import sys

from curio import Kernel, Event, spawn, socket, ssl

import h2.config
import h2.connection
import h2.events


# The maximum amount of a file we'll send in a single DATA frame.
from hyper2web import endpoint
from hyper2web.endpoint import EndPointHandler

READ_CHUNK_SIZE = 8192


def create_listening_ssl_socket(address, certfile, keyfile):
    """
    Create and return a listening TLS socket on a given address.
    """
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.options |= (
        ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_COMPRESSION
    )
    ssl_context.set_ciphers("ECDHE+AESGCM")
    ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    ssl_context.set_alpn_protocols(["h2"])

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock = ssl_context.wrap_socket(sock)
    sock.bind(address)
    sock.listen()

    return sock


async def h2_server(address, root, certfile, keyfile, app):
    """
    Create an HTTP/2 server at the given address.
    """
    sock = create_listening_ssl_socket(address, certfile, keyfile)
    print("Now listening on %s:%d" % address)

    async with sock:
        while True:
            client, _ = await sock.accept()
            server = H2Server(client, root, app)
            app.server = server
            await spawn(server.run())


class H2Server:
    """
    A basic HTTP/2 file server. This is essentially very similar to
    SimpleHTTPServer from the standard library, but uses HTTP/2 instead of
    HTTP/1.1.
    """
    def __init__(self, sock, root, app):
        config = h2.config.H2Configuration(client_side=False, header_encoding='utf-8')
        self.sock = sock
        self.conn = h2.connection.H2Connection(config=config)
        self.root = root
        self.flow_control_events = {}

        # the Application that needs this server
        # this server runs this app
        self.app = app

    async def run(self):
        """
        Loop over the connection, managing it appropriately.
        """
        self.conn.initiate_connection()
        await self.sock.sendall(self.conn.data_to_send())

        while True:
            # 65535 is basically arbitrary here: this amounts to "give me
            # whatever data you have".
            data = await self.sock.recv(65535)
            if not data:
                break

            events = self.conn.receive_data(data)
            for event in events:

                if isinstance(event, h2.events.RequestReceived):
                    await spawn(self.request_received(event))

                elif isinstance(event, h2.events.DataReceived):
                    print('DataReceived')
                    # self.conn.reset_stream(event.stream_id)
                    await spawn(self.data_received(event))
                elif isinstance(event, h2.events.WindowUpdated):
                    await self.window_updated(event)

            await self.sock.sendall(self.conn.data_to_send())

    async def data_received(self, event: h2.events.DataReceived):
        """
        Handle received data for a certain stream. Currently used for POST
        """
        if event.stream_id not in endpoint.active_end_points:
            # But I think this situation is impossible since header should always arrive before data
            print('data before header')
            # raise Exception('data before header')
            # create a new endpoint
            endpoint.active_end_points[event.stream_id] = EndPointHandler(self, self.sock, self.conn, event.stream_id)

        # update this handler
        print('xxx')
        endpoint.active_end_points[event.stream_id].update(event)
        print('xxx2')
        # possibly finalize this handler
        if event.stream_ended:
            print('xxx3')
            print(event.stream_id in endpoint.active_end_points)
            endpoint.active_end_points[event.stream_id].finalize()
            print('xxx4')
            await self.app.handle_route(endpoint.active_end_points[event.stream_id])
            print('xxx5')
            del endpoint.active_end_points[event.stream_id]
            print('xxx6')
        print('xxx7')
    # todo: should not directly call handle_route in this function
    # todo: since a handler may not be finalized
    async def request_received(self, event: h2.events.RequestReceived):
        """
        Handle a request
        """
        headers = dict(event.headers)
        stream_id = event.stream_id
        route = headers[':path'].lstrip('/')

        endpoint_handler = EndPointHandler(self, self.sock, self.conn, stream_id=stream_id, header=headers, route=route)

        if headers[':method'] == 'GET':
            # it's fine to call handle_route for GET since header is the only thing needed
            print('1')
            await self.app.handle_route(endpoint_handler)

        elif headers[':method'] == 'POST':
            if stream_id in endpoint.active_end_points:
                print('should not be')
                raise Exception('should not be')
            endpoint.active_end_points[stream_id] = endpoint_handler

        elif headers[':method'] == 'PUT':
            raise NotImplementedError('PUT is not implemented yet')

        elif headers[':method'] == 'DELETE':
            raise NotImplementedError('DELETE is not implemented yet')

        else:
            raise NotImplementedError(headers[':method']+' is not implemented')

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
