

import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl

KEYFILE = 'key.pem'
CERTFILE = 'cert.pem'

def echo_client(s):
    while True:
        data = s.recv(8192)
        print(data.decode("utf-8"))
        if data == b'':
            break
        s.send(b'This is a response.')
        print('Connection closed')
    s.close()

def echo_server(address):
    s = socket.socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(1)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    s_ssl = ssl.wrap_socket(s, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)

    while True:
        try:
            (c,a) = s_ssl.accept()
            print('Got connection', c, a)
            echo_client(c)
        except socket.error as e:
            print('Error: {0}'.format(e))

echo_server((socket.gethostbyname('localhost'), 8082))
