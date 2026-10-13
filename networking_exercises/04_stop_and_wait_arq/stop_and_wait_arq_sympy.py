from sympy import Integer

def server(data):
    frames = data.get("frames", ["Frame A", "Frame B", "Frame C"])
    lost_ack = set(data.get("lost_ack", []))
    events = []
    sequence = Integer(0)

    for number, frame in enumerate(frames):
        events.append(f"Send frame {sequence}: {frame}")
        if number in lost_ack:
            events.append(f"ACK {sequence} lost; timeout")
            events.append(f"Retransmit frame {sequence}: {frame}")
        events.append(f"ACK {sequence} received")
        sequence = 1 - sequence

    return {"events": events}


def client(data):
    return server(data)


def print_result(result):
    print("Stop-and-Wait ARQ:")
    for event in result["events"]:
        print(event)


def main():
    sample = {'frames': ['Hello', 'Network', 'Lab'], 'lost_ack': [1]}
    print_result(client(sample))


if __name__ == "__main__":
    main()
