import ssl

port = 8082

import socket, ssl

while True:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Require a certificate from the server. We used a self-signed certificate
    # so here ca_certs must be the server certificate itself.
    ssl_sock = ssl.wrap_socket(s,cert_reqs=ssl.CERT_REQUIRED, ca_certs='cert.pem')

    ssl_sock.connect(('127.0.0.1', 8082))

    ssl_sock.write(str(input("Enter Something: ")).encode())

    ssl_sock.close()
