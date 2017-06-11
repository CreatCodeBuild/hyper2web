"""
A fully-functional HTTP/2 server written for curio.

Requires Python 3.5+.
"""

from curio import spawn, socket

import h2.config
import h2.connection
import h2.events

# hyper2web imports
from . import sslsocket, abstract, http
create_listening_ssl_socket = sslsocket.create_listening_ssl_socket
HTTP = http.HTTP


# todo: move this to app.App
async def h2_server(address, certfile, keyfile, app: abstract.AbstractApp):
    """
    Create an HTTP/2 server at the given address.
    """
    sock = create_listening_ssl_socket(address, certfile, keyfile)
    print("Now listening on %s:%d" % address)

    async with sock:
        while True:
            client, _ = await sock.accept()
            server = H2Server(client, app)
            await spawn(server.run())


class H2Server:
    """
    This class just connects to socket and that's about it.
    Most heavy lifting is done by http.HTTP
    """
    def __init__(self, sock, app: abstract.AbstractApp):
        config = h2.config.H2Configuration(client_side=False, header_encoding='utf-8')
        self.sock = sock
        self.conn = h2.connection.H2Connection(config=config)

        # the Application that needs this server
        # this server runs this app
        self.http = HTTP(app=app, sock=self.sock, connection=self.conn)

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
                await self.http.handle_event(event)

            await self.sock.sendall(self.conn.data_to_send())
