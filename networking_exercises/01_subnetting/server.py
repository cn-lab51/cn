import json
import socket

HOST = "127.0.0.1"
PORT = 5500

import ipaddress

def calculate(data):
    network = ipaddress.ip_network(f"{data['ip']}/{data.get('prefix', 24)}", strict=False)
    if network.version != 4:
        raise ValueError("IPv4 address required")
    hosts = list(network.hosts())
    if not hosts:
        raise ValueError("Network has no usable host addresses")
    return {"network": str(network.network_address), "broadcast": str(network.broadcast_address), "first_usable": str(hosts[0]), "last_usable": str(hosts[-1]), "prefix": network.prefixlen}

def handle(connection):
    with connection:
        raw = connection.makefile("rb").readline()
        try:
            request = json.loads(raw.decode("utf-8"))
            response = {"ok": True, "result": calculate(request)}
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
