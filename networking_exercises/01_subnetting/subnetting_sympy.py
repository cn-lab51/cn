import ipaddress
from sympy import And, Eq, Implies, Integer, Mod, Symbol, false, simplify, simplify_logic, true

def calculate(ip, prefix=24):
    address = ipaddress.IPv4Address(ip)
    if not 0 <= prefix <= 32:
        raise ValueError("Prefix must be from 0 to 32")
    network = ipaddress.ip_network(f"{address}/{prefix}", strict=False)
    hosts = list(network.hosts())
    if not hosts:
        raise ValueError("Network has no usable host addresses")
    return {"network": str(network.network_address), "broadcast": str(network.broadcast_address), "first_usable": str(hosts[0]), "last_usable": str(hosts[-1]), "prefix": prefix}

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
    result = client(calculate, **{'ip': '192.168.1.25', 'prefix': 24})
    print(format_result(result))

if __name__ == "__main__":
    main()
