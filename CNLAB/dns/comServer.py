
import socket

HOST = "127.0.0.1"
PORT = 12347

AUTH_ADDR = {
    "example": "('127.0.0.1', 12348)",
    "arjun": "('127.0.0.1', 13447)"
}

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(".com TLD server started")

        while True:
            conn, addr = s.accept()
            with conn:
                print("Connection", addr, "accepted")
                url = conn.recv(1024).decode().strip().lower()
                auth = url.split(".")[-2]
                response = AUTH_ADDR.get(auth, "")
                conn.sendall(response.encode())
                print("Sent response:", auth, response)

if __name__ == "__main__":
    main()
