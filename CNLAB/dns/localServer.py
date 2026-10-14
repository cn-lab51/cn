
import socket
import ast

HOST = "127.0.0.1"
PORT = 12345
ROOT_ADDR = ("127.0.0.1", 12346)
CACHE = {}

def query_server(url, addr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ts:
        ts.settimeout(5)
        ts.connect(addr)
        print("Connected to", addr)
        ts.sendall(url.encode())
        return ts.recv(1024).decode()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Recursive DNS server started")

        while True:
            conn, addr = s.accept()
            with conn:
                print("Connection", addr, "accepted")
                url = conn.recv(1024).decode().strip().lower()

                try:
                    if url in CACHE:
                        print("CACHE HIT on", url)
                        domain_addr = CACHE[url]
                    else:
                        print("CACHE MISS on", url)
                        tld_addr = ast.literal_eval(query_server(url, ROOT_ADDR))
                        auth_addr = ast.literal_eval(query_server(url, tld_addr))
                        domain_addr = query_server(url, auth_addr)
                        CACHE[url] = domain_addr

                    conn.sendall(domain_addr.encode())
                    print("Sent data:", domain_addr)
                except (OSError, ValueError, SyntaxError, KeyError, IndexError):
                    conn.sendall(b"Domain not found or server unavailable")

if __name__ == "__main__":
    main()
