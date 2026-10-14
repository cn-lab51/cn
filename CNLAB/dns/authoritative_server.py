import socket

s = socket.socket()
s.bind(("127.0.0.1", 5003))
s.listen()

domains = {
    "example.com": "93.184.216.34",
    "google.com": "142.250.190.14"
}

while True:
    conn, addr = s.accept()
    domain = conn.recv(1024).decode()

    conn.send(domains.get(domain, "Not Found").encode())
    conn.close()
