import json
import socket

HOST = "127.0.0.1"
PORT = 5503

def print_result(result):
    print("Stop-and-Wait ARQ:")
    for event in result["events"]:
        print(event)


def main():
    request = {'frames': ['Hello', 'Network', 'Lab'], 'lost_ack': [1]}
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as connection:
            connection.sendall((json.dumps(request) + "\n").encode("utf-8"))
            reader = connection.makefile("r", encoding="utf-8")
            reply = json.loads(reader.readline())
    except OSError as error:
        print(f"Could not connect to the server: {error}")
        return

    if not reply["ok"]:
        print(f"Server error: {reply['error']}")
        return
    print_result(reply["result"])


if __name__ == "__main__":
    main()
