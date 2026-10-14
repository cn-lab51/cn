import socket

domain = input("Enter domain: ")

s = socket.socket()
s.connect(("127.0.0.1", 5000))
s.send(domain.encode())

print("IP Address:", s.recv(1024).decode())
s.close()