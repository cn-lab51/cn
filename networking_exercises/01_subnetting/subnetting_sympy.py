import ipaddress
from sympy import Integer

def server(data):
    ip = ipaddress.IPv4Address(data["ip"])
    prefix = int(data.get("prefix", 24))
    if not 0 <= prefix <= 30:
        raise ValueError("Use a prefix from 0 to 30 for usable host addresses")

    host_count = Integer(2) ** (32 - prefix)
    address_number = Integer(int(ip))
    network_number = address_number // host_count * host_count
    broadcast_number = network_number + host_count - 1

    return {
        "network": str(ipaddress.IPv4Address(int(network_number))),
        "prefix": prefix,
        "first": str(ipaddress.IPv4Address(int(network_number + 1))),
        "last": str(ipaddress.IPv4Address(int(broadcast_number - 1))),
        "broadcast": str(ipaddress.IPv4Address(int(broadcast_number))),
    }


def client(data):
    return server(data)


def print_result(result):
    print(f"Network: {result['network']}/{result['prefix']}")
    print(f"First usable IP: {result['first']}")
    print(f"Last usable IP: {result['last']}")
    print(f"Broadcast address: {result['broadcast']}")


def main():
    sample = {'ip': '192.168.1.25', 'prefix': 24}
    print_result(client(sample))


if __name__ == "__main__":
    main()
