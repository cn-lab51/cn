
import socket

name = input("Enter client name (A or B): ").strip().upper()
if name not in ("A", "B"):
    raise SystemExit("Enter A or B")

bit = input("Enter data bit (0 or 1): ").strip()
if bit not in ("0", "1"):
    raise SystemExit("Enter 0 or 1")

s = socket.socket()
s.connect(("127.0.0.1", 5004))
s.sendall((name + " " + bit).encode())
print(s.recv(1024).decode())
s.close()
