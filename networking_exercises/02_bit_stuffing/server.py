import json
import socket

HOST = "127.0.0.1"
PORT = 5501

def process(data):
    bits = data["bits"]
    if not bits or any(bit not in "01" for bit in bits):
        raise ValueError("bits must be a nonempty binary string")
    threshold = int(data.get("threshold", 5))
    stuffed = []
    ones = 0
    for bit in bits:
        stuffed.append(bit)
        if bit == "1":
            ones += 1
            if ones == threshold:
                stuffed.append("0")
                ones = 0
        else:
            ones = 0
    encoded = "".join(stuffed)
    return {"input": bits, "stuffed": encoded, "destuffed": destuff(encoded, threshold)}

def destuff(bits, threshold=5):
    out = []
    ones = 0
    i = 0
    while i < len(bits):
        bit = bits[i]
        out.append(bit)
        if bit == "1":
            ones += 1
            if ones == threshold:
                i += 1
                if i >= len(bits) or bits[i] != "0":
                    raise ValueError("missing stuffed zero")
                ones = 0
        else:
            ones = 0
        i += 1
    return "".join(out)

def handle(connection):
    with connection:
        raw = connection.makefile("rb").readline()
        try:
            request = json.loads(raw.decode("utf-8"))
            response = {"ok": True, "result": process(request)}
        except Exception as error:
            response = {"ok": False, "error": str(error)}
        connection.sendall((json.dumps(response) + "\n").encode("utf-8"))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            connection, _ = server.accept()
            handle(connection)

if __name__ == "__main__":
    main()
