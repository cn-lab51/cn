
import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 5003))
s.listen(1)
print("Server started")

c, addr = s.accept()
f = c.makefile("r")

while True:
    line = f.readline()
    if not line:
        break
    line = line.strip()
    if line == "END":
        break
    seq, data = line.split("|", 1)
    print("Received frame", seq, ":", data)
    c.sendall(("ACK " + seq + "\n").encode())

c.close()
s.close()
