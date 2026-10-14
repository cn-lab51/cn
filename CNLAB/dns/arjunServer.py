
import socket

HOST = "127.0.0.1"
PORT = 13447

RECORDS = {
    "www": "www.arjun.com | ('143.76.76.100', 65432)",
    "services": "services.arjun.com | ('45.5.9.110', 15447)"
}

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Arjun authoritative server started")

        while True:
            conn, addr = s.accept()
            with conn:
                print("Connection", addr, "accepted")
                url = conn.recv(1024).decode().strip().lower()
                domain = url.split(".")[-3]
                response = RECORDS.get(domain, "Domain not found")
                conn.sendall(response.encode())
                print("Sent response:", domain, response)

if __name__ == "__main__":
    main()
