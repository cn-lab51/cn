import ipaddress
from sympy import Integer

RECORDS = {
    "www.example.com": "93.184.216.34",
    "lab.example.org": "203.0.113.25",
}


def server(data):
    domain = data["domain"].strip(".").lower()
    if domain not in RECORDS:
        raise ValueError("That name is not in the sample DNS table")

    parts = domain.split(".")
    zone = ".".join(parts[-2:])
    ip = RECORDS[domain]
    path = [
        "Client asks the recursive resolver",
        "Resolver asks a root server",
        f"Root server points to the .{parts[-1]} TLD server",
        f"TLD server points to the {zone} authoritative server",
        "Authoritative server returns the address",
        "Resolver returns the answer to the client",
    ]
    address_number = Integer(int(ipaddress.IPv4Address(ip)))
    return {"domain": domain, "ip": ip, "path": path, "address_number": int(address_number)}


def client(data):
    return server(data)


def print_result(result):
    print("Recursive DNS lookup:")
    for step in result["path"]:
        print(step)
    print(f"Answer: {result['domain']} -> {result['ip']}")


def main():
    sample = {'domain': 'www.example.com'}
    print_result(client(sample))


if __name__ == "__main__":
    main()
