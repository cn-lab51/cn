import json
import socket
from sympy import FiniteSet, Integer

HOST = "127.0.0.1"
PORT = 5502

TABLE = {
    "02:00:5e:10:00:01": "192.168.1.10",
    "02:00:5e:10:00:02": "192.168.1.11",
    "02:00:5e:10:00:03": "192.168.1.12",
}


def lookup(data):
    mac = data["mac"].lower()
    registered_macs = FiniteSet(*(Integer(int(item.replace(":", ""), 16)) for item in TABLE))
    mac_number = Integer(int(mac.replace(":", ""), 16))
    if mac_number not in registered_macs:
        raise ValueError("That MAC address is not in the sample table")
    return {"mac": mac, "ip": TABLE[mac]}


def handle_client(connection):
    with connection:
        try:
            reader = connection.makefile("r", encoding="utf-8")
            request = json.loads(reader.readline())
            reply = {"ok": True, "result": lookup(request)}
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
