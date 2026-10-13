import json
import socket


HOST = "127.0.0.1"
PORT = 5504

def transmit(data):
    clients = data["clients"]
    names = list(clients)
    if not names:
        raise ValueError("Add at least one client")

    size = len(clients[names[0]]["code"])
    signal = [0] * size
    for client in clients.values():
        code = client["code"]
        bit = client["bit"]
        if len(code) != size or bit not in (-1, 1):
            raise ValueError("Use equal-length codes and data bits of 1 or -1")
        if any(chip not in (-1, 1) for chip in code):
            raise ValueError("Each chip must be 1 or -1")
        signal = [total + bit * chip for total, chip in zip(signal, code)]

    recovered = {}
    for name, client in clients.items():
        code = client["code"]
        for other_name, other in clients.items():
            if name != other_name and sum(a * b for a, b in zip(code, other["code"])) != 0:
                raise ValueError("Client codes must be orthogonal")
        score = sum(value * chip for value, chip in zip(signal, code))
        recovered[name] = 1 if score > 0 else -1 if score < 0 else 0

    return {"signal": signal, "recovered": recovered}


def handle_client(connection):
    with connection:
        try:
            reader = connection.makefile("r", encoding="utf-8")
            request = json.loads(reader.readline())
            reply = {"ok": True, "result": transmit(request)}
        except (KeyError, TypeError, ValueError) as error:
            reply = {"ok": False, "error": str(error)}
        connection.sendall((json.dumps(reply) + "\n").encode("utf-8"))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Listening on {HOST}:{PORT}")
        while True:
            connection, _ = server.accept()
            handle_client(connection)


if __name__ == "__main__":
    main()
