import json
import socket

HOST = "127.0.0.1"
PORT = 5505

RECORDS = {"www.example.com": "93.184.216.34", "lab.example.org": "203.0.113.25"}

def resolve(data):
    domain = data["domain"].strip(".").lower()
    labels = domain.split(".")
    if len(labels) < 2 or any(not label for label in labels):
        raise ValueError("enter a valid domain such as www.example.com")
    if domain not in RECORDS:
        raise ValueError("domain is not present in the sample DNS zone")
    tld = labels[-1]
    authoritative = ".".join(labels[-2:])
    return {"domain": domain, "query_path": ["Client -> Recursive resolver", "Recursive resolver -> Root server", f"Root -> {tld.upper()} TLD server", f"{tld.upper()} TLD -> Authoritative server for {authoritative}", "Authoritative server -> Recursive resolver", "Recursive resolver -> Client"], "ip": RECORDS[domain]}

def handle(connection):
    with connection:
        raw = connection.makefile("rb").readline()
        try:
            request = json.loads(raw.decode("utf-8"))
            response = {"ok": True, "result": resolve(request)}
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
