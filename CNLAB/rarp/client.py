
import socket

s = socket.socket()
s.connect(("127.0.0.1", 5002))
mac = input("Enter MAC address: ")
s.sendall(mac.encode())
print("IP address:", s.recv(1024).decode())
s.close()
