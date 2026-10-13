import json
import socket

HOST = "127.0.0.1"
PORT = 5504

def encode(data):
    clients = data.get("clients", {"A": {"bit": 1, "code": [1, -1, 1, -1]}, "B": {"bit": -1, "code": [1, 1, -1, -1]}})
    names = list(clients)
    if not names:
        raise ValueError("at least one client is required")
    length = len(clients[names[0]]["code"])
    if length == 0 or any(len(item["code"]) != length for item in clients.values()):
        raise ValueError("all chipping codes must have equal nonzero length")
    signal = [0] * length
    for item in clients.values():
        if item["bit"] not in (-1, 1) or any(chip not in (-1, 1) for chip in item["code"]):
            raise ValueError("data bits and chips must be -1 or 1")
        signal = [s + item["bit"] * chip for s, chip in zip(signal, item["code"])]
    extracted = {}
    for name, item in clients.items():
        dot = sum(s * chip for s, chip in zip(signal, item["code"]))
        extracted[name] = 1 if dot > 0 else -1 if dot < 0 else 0
    return {"clients": clients, "composite_signal": signal, "extracted_bits": extracted}

def handle(connection):
    with connection:
        raw = connection.makefile("rb").readline()
        try:
            request = json.loads(raw.decode("utf-8"))
            response = {"ok": True, "result": encode(request)}
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
