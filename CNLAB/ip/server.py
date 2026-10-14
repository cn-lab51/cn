
import socket
import ipaddress

s = socket.socket()
s.bind(("127.0.0.1", 5000))
s.listen(5)
print("Server started")

while True:
    c, addr = s.accept()
    ip = c.recv(1024).decode()
    net = ipaddress.ip_network(ip + "/24", strict=False)
    first = net.network_address + 1
    last = net.broadcast_address - 1
    result = "First usable IP: " + str(first) + "\nLast usable IP: " + str(last)
    c.send(result.encode())
    c.close()
