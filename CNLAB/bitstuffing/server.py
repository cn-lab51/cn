
import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 5001))
s.listen(1)
print("Server started")

c, addr = s.accept()
data = c.recv(1024).decode().strip()

if not data or any(x not in "01" for x in data):
    c.sendall("Invalid bit string".encode())
else:
    stuffed = ""
    count = 0
    for bit in data:
        stuffed += bit
        if bit == "1":
            count += 1
            if count == 5:
                stuffed += "0"
                count = 0
        else:
            count = 0

    original = ""
    count = 0
    i = 0
    while i < len(stuffed):
        bit = stuffed[i]
        original += bit
        if bit == "1":
            count += 1
            if count == 5:
                i += 1
                count = 0
        else:
            count = 0
        i += 1

    result = "Stuffed: " + stuffed + "\nDestuffed: " + original
    c.sendall(result.encode())

c.close()
s.close()
