
import socket
s = socket.socket()
s.connect(("127.0.0.1", 5003))
f = s.makefile("r")

frames = ["Hello", "Computer", "Networks", "Done"]

for i, data in enumerate(frames):
    s.sendall((str(i % 2) + "|" + data + "\n").encode())
    ack = f.readline().strip()
    print("Sent:", data, "Received:", ack)

s.sendall(b"END\n")
s.close()
