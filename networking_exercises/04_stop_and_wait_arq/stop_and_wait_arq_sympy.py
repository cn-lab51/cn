import ipaddress
from sympy import And, Eq, Implies, Integer, Mod, Symbol, false, simplify, simplify_logic, true

def transmit(frames, lost_ack_frames=()):
    lost = set(int(i) for i in lost_ack_frames)
    events = []
    seq_symbol = Symbol("sequence_number", integer=True, nonnegative=True)
    sequence_rule = Eq(Mod(seq_symbol, 2), seq_symbol % 2)
    for seq, payload in enumerate(frames):
        events.append(f"Sender -> Frame {seq}: {payload}")
        events.append(f"Receiver -> ACK {seq}")
        if seq in lost:
            events.append(f"ACK {seq} lost; sender timeout")
            events.append(f"Sender -> Retransmit Frame {seq}: {payload}")
            events.append(f"Receiver -> ACK {seq}")
        events.append(f"Sender -> Frame {seq + 1} allowed")
    return {"frames_sent": len(frames), "events": events, "sympy_sequence_rule": str(sequence_rule)}

def client(server_function, *args, **kwargs):
    return server_function(*args, **kwargs)

def format_result(result):
    if "first_usable" in result:
        return f"Network: {result['network']}/{result['prefix']}\nFirst usable IP: {result['first_usable']}\nLast usable IP: {result['last_usable']}\nBroadcast address: {result['broadcast']}"
    if "stuffed" in result:
        return f"Original bits: {result['input']}\nAfter bit stuffing: {result['stuffed']}\nAfter destuffing: {result['destuffed']}"
    if "mac" in result:
        return f"MAC address: {result['mac']}\nAssigned IP address: {result['ip']}"
    if "events" in result:
        return "Stop-and-Wait ARQ transmission:\n" + "\n".join(result["events"])
    if "composite_signal" in result:
        recovered = ", ".join(f"Client {name}: {bit:+d}" for name, bit in result["extracted_bits"].items())
        return f"Composite signal: {result['composite_signal']}\nRecovered data bits: {recovered}"
    if "query_path" in result:
        return "Recursive DNS lookup:\n" + "\n".join(result["query_path"]) + f"\nResolved address: {result['domain']} -> {result['ip']}"
    return str(result)

def main():
    result = client(transmit, **{'frames': ['Hello', 'Network', 'Lab'], 'lost_ack_frames': [1]})
    print(format_result(result))

if __name__ == "__main__":
    main()
