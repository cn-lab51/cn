
import socket

HOST = "127.0.0.1"
PORT = 12345

def main():
    url = input("Enter the URL to resolve: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((HOST, PORT))
        s.sendall(url.encode())
        ip = s.recv(1024).decode()
        print(ip)

if __name__ == "__main__":
    main()
