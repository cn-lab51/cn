
import socket

codes = {
    "A": [1, 1, 1, 1],
    "B": [1, -1, 1, -1]
}

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 5004))
s.listen(2)
print("CDMA Server started")

clients = {}
bits = {}

for i in range(2):
    c, addr = s.accept()
    msg = c.recv(1024).decode().strip().split()
    name, bit = msg
    if name not in codes or name in clients or bit not in ("0", "1"):
        c.sendall(b"Invalid client or bit")
        c.close()
        s.close()
        raise SystemExit
    clients[name] = c
    bits[name] = 1 if bit == "1" else -1

signal = [
    bits["A"] * codes["A"][i] + bits["B"] * codes["B"][i]
    for i in range(4)
]

print("Combined signal:", signal)

decoded = {}
for name in codes:
    value = sum(signal[i] * codes[name][i] for i in range(4)) // 4
    decoded[name] = "1" if value > 0 else "0"

for name, c in clients.items():
    result = "Decoded A: " + decoded["A"] + "\nDecoded B: " + decoded["B"]
    c.sendall(result.encode())
    c.close()

s.close()
