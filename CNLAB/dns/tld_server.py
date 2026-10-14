import socket

s = socket.socket()
s.bind(("127.0.0.1", 5002))
s.listen()

while True:
    conn, addr = s.accept()
    domain = conn.recv(1024).decode()

    next_server = socket.socket()
    next_server.connect(("127.0.0.1", 5003))
    next_server.send(domain.encode())

    result = next_server.recv(1024).decode()
    next_server.close()

    conn.send(result.encode())
    conn.close()