import json
import socket


HOST = "127.0.0.1"
PORT = 5503

def transmit(data):
    frames = data.get("frames", ["Frame A", "Frame B", "Frame C"])
    lost_ack = set(data.get("lost_ack", []))
    events = []
    sequence = 0

    for number, frame in enumerate(frames):
        events.append(f"Send frame {sequence}: {frame}")
        if number in lost_ack:
            events.append(f"ACK {sequence} lost; timeout")
            events.append(f"Retransmit frame {sequence}: {frame}")
        events.append(f"ACK {sequence} received")
        sequence = 1 - sequence

    return {"events": events}


def handle_client(connection):
    with connection:
        try:
            reader = connection.makefile("r", encoding="utf-8")
            request = json.loads(reader.readline())
            reply = {"ok": True, "result": transmit(request)}
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
