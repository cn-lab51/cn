import socket
import threading

s = socket.socket()
s.bind(("127.0.0.1", 5000))
s.listen()

def handle_client(conn):
    domain = conn.recv(1024).decode()

    next_server = socket.socket()
    next_server.connect(("127.0.0.1", 5001))
    next_server.send(domain.encode())

    result = next_server.recv(1024).decode()
    next_server.close()

    conn.send(result.encode())
    conn.close()

while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_client, args=(conn,)).start()