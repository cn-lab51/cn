import ipaddress
from sympy import And, Eq, Implies, Integer, Mod, Symbol, false, simplify, simplify_logic, true

TABLE = {"02:00:5e:10:00:01": "192.168.1.10", "02:00:5e:10:00:02": "192.168.1.11", "02:00:5e:10:00:03": "192.168.1.12"}

def lookup(mac):
    normalized = mac.lower()
    if normalized not in TABLE:
        raise ValueError("MAC address is not registered in the sample RARP table")
    match = Symbol("mac_match")
    rule = Implies(match, true)
    return {"mac": normalized, "ip": TABLE[normalized], "sympy_rule": str(rule)}

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
    result = client(lookup, **{'mac': '02:00:5e:10:00:01'})
    print(format_result(result))

if __name__ == "__main__":
    main()
