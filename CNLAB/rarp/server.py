
import socket
table = {
    "AA:BB:CC:DD:EE:01": "192.168.1.10",
    "AA:BB:CC:DD:EE:02": "192.168.1.20",
    "AA:BB:CC:DD:EE:03": "192.168.1.30"
}
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 5002))
s.listen(5)
print("RARP Server started")

while True:
    c, addr = s.accept()
    mac = c.recv(1024).decode().strip().upper()
    ip = table.get(mac, "MAC address not found")
    c.sendall(ip.encode())
    c.close()
