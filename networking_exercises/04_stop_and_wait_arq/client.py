import json
import socket

HOST = "127.0.0.1"
PORT = 5503


def format_result(response):
    if not response.get("ok"):
        return f"Error: {response.get('error', 'unknown server error')}"
    result = response["result"]
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
    request = {'frames': ['Hello', 'Network', 'Lab'], 'lost_ack_frames': [1]}
    with socket.create_connection((HOST, PORT), timeout=5) as connection:
        connection.sendall((json.dumps(request) + "\n").encode("utf-8"))
        response = json.loads(connection.makefile("rb").readline().decode("utf-8"))
    print(format_result(response))

if __name__ == "__main__":
    main()
