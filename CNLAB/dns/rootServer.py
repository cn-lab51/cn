
import socket

HOST = "127.0.0.1"
PORT = 12346

TLD_ADDR = {
    "com": "('127.0.0.1', 12347)"
}

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("Root DNS server started")

        while True:
            conn, addr = s.accept()
            with conn:
                print("Connection", addr, "accepted")
                url = conn.recv(1024).decode().strip().lower()
                tld = url.split(".")[-1]
                response = TLD_ADDR.get(tld, "")
                conn.sendall(response.encode())
                print("Sent response:", tld, response)

if __name__ == "__main__":
    main()
