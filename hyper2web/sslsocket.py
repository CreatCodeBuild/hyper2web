import os

from curio import socket, ssl


def create_listening_ssl_socket(address, certfile, keyfile):
    """
    Create and return a listening TLS socket on a given address.
    """
    # check if 2 files exist. If not, raise exceptions
    if os.path.isfile(certfile) and os.path.isfile(keyfile):
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
    else:
        raise FileNotFoundError(certfile + " and/or " + keyfile + " don't exist. HTTP/2 needs certificate files.")
