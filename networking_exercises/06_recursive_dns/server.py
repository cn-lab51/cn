import json
import socket


HOST = "127.0.0.1"
PORT = 5505

RECORDS = {
    "www.example.com": "93.184.216.34",
    "lab.example.org": "203.0.113.25",
}


def resolve(data):
    domain = data["domain"].strip(".").lower()
    if domain not in RECORDS:
        raise ValueError("That name is not in the sample DNS table")

    parts = domain.split(".")
    zone = ".".join(parts[-2:])
    path = [
        "Client asks the recursive resolver",
        "Resolver asks a root server",
        f"Root server points to the .{parts[-1]} TLD server",
        f"TLD server points to the {zone} authoritative server",
        "Authoritative server returns the address",
        "Resolver returns the answer to the client",
    ]
    return {"domain": domain, "ip": RECORDS[domain], "path": path}


def handle_client(connection):
    with connection:
        try:
            reader = connection.makefile("r", encoding="utf-8")
            request = json.loads(reader.readline())
            reply = {"ok": True, "result": resolve(request)}
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
