
import socket

s = socket.socket()
s.connect(("127.0.0.1", 5000))
ip = input("Enter IP address: ")
s.send(ip.encode())
result = s.recv(1024).decode()
print(result)
s.close()
