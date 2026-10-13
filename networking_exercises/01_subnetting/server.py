import json
import socket
import ipaddress

HOST = "127.0.0.1"
PORT = 5500

def calculate(data):
    ip = ipaddress.IPv4Address(data["ip"])
    prefix = int(data.get("prefix", 24))
    if not 0 <= prefix <= 30:
        raise ValueError("Use a prefix from 0 to 30 for usable host addresses")

    network = ipaddress.ip_network(f"{ip}/{prefix}", strict=False)
    return {
        "network": str(network.network_address),
        "prefix": prefix,
        "first": str(network.network_address + 1),
        "last": str(network.broadcast_address - 1),
        "broadcast": str(network.broadcast_address),
    }


def handle_client(connection):
    with connection:
        try:
            reader = connection.makefile("r", encoding="utf-8")
            request = json.loads(reader.readline())
            reply = {"ok": True, "result": calculate(request)}
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
