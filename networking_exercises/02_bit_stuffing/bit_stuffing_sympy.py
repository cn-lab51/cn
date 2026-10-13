import ipaddress
from sympy import And, Eq, Implies, Integer, Mod, Symbol, false, simplify, simplify_logic, true

def process(bits, threshold=5):
    if not bits or any(bit not in "01" for bit in bits):
        raise ValueError("bits must be a nonempty binary string")
    stuffed = []
    run = 0
    for bit in bits:
        stuffed.append(bit)
        run = run + 1 if bit == "1" else 0
        if run == threshold:
            stuffed.append("0")
            run = 0
    encoded = "".join(stuffed)
    decoded = destuff(encoded, threshold)
    return {"input": bits, "stuffed": encoded, "destuffed": decoded, "sympy_boolean_check": simplify_logic(And(*[true if b == "1" else false for b in bits])) if len(bits) < 20 else "skipped for long input"}

def destuff(bits, threshold=5):
    out = []
    run = 0
    i = 0
    while i < len(bits):
        bit = bits[i]
        out.append(bit)
        run = run + 1 if bit == "1" else 0
        if run == threshold:
            i += 1
            if i >= len(bits) or bits[i] != "0":
                raise ValueError("missing stuffed zero")
            run = 0
        i += 1
    return "".join(out)

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
    result = client(process, **{'bits': '1111101111110', 'threshold': 5})
    print(format_result(result))

if __name__ == "__main__":
    main()
