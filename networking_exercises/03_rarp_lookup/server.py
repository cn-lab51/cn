import json
import socket

HOST = "127.0.0.1"
PORT = 5502

TABLE = {"02:00:5e:10:00:01": "192.168.1.10", "02:00:5e:10:00:02": "192.168.1.11", "02:00:5e:10:00:03": "192.168.1.12"}

def lookup(data):
    mac = data["mac"].lower()
    if mac not in TABLE:
        raise ValueError("MAC address is not registered in the sample RARP table")
    return {"mac": mac, "ip": TABLE[mac]}

def handle(connection):
    with connection:
        raw = connection.makefile("rb").readline()
        try:
            request = json.loads(raw.decode("utf-8"))
            response = {"ok": True, "result": lookup(request)}
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
