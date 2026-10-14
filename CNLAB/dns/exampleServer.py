
import socket

HOST = "127.0.0.1"
PORT = 12348

RECORDS = {
    "www": "www.example.com | ('192.168.1.11', 12349)",
    "products": "products.example.com | ('100.5.6.17', 15447)"
}

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Example authoritative server started")

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
