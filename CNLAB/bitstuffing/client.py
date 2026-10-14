
import socket

s = socket.socket()
s.connect(("127.0.0.1", 5001))
bits = input("Enter bit string: ")
s.sendall(bits.encode())
print(s.recv(1024).decode())
s.close()
