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
                    self.conn.reset_stream(event.stream_id)

                elif isinstance(event, h2.events.WindowUpdated):
                    await self.window_updated(event)

            await self.sock.sendall(self.conn.data_to_send())

    async def request_received(self, event):
        """
        Handle a request
        """
        headers = dict(event.headers)
        stream_id = event.stream_id
        endpoint = EndPointHandler(self, self.sock, self.conn, stream_id)

        if headers[':method'] == 'GET':
            route = headers[':path'].lstrip('/')
            
            if route in self.app.routes['GET']:
                await self.app.routes['GET'][route](endpoint)

            else:
                # if route is not registered, assume it is requesting files
                full_path = os.path.join(self.root, route)
                if os.path.exists(full_path):
                    await endpoint.send_file(full_path)
                else:
                    await endpoint.send_error(404)

        elif headers[':method'] == 'POST':
            raise NotImplementedError('Only GET is implemented')

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
