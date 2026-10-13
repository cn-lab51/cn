import json
import socket

HOST = "127.0.0.1"
PORT = 5503

def transmit(data):
    frames = data.get("frames", ["Frame 0", "Frame 1", "Frame 2"])
    lost = set(int(i) for i in data.get("lost_ack_frames", []))
    events = []
    for seq, payload in enumerate(frames):
        events.append(f"Sender -> Frame {seq}: {payload}")
        events.append(f"Receiver -> ACK {seq}")
        if seq in lost:
            events.append(f"ACK {seq} lost; sender timeout")
            events.append(f"Sender -> Retransmit Frame {seq}: {payload}")
            events.append(f"Receiver -> ACK {seq}")
        events.append(f"Sender -> Frame {seq + 1} allowed")
    return {"frames_sent": len(frames), "events": events}

def handle(connection):
    with connection:
        raw = connection.makefile("rb").readline()
        try:
            request = json.loads(raw.decode("utf-8"))
            response = {"ok": True, "result": transmit(request)}
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
