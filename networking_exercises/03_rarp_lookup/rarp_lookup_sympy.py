from sympy import FiniteSet, Integer

TABLE = {
    "02:00:5e:10:00:01": "192.168.1.10",
    "02:00:5e:10:00:02": "192.168.1.11",
    "02:00:5e:10:00:03": "192.168.1.12",
}


def server(data):
    mac = data["mac"].lower()
    mac_number = Integer(int(mac.replace(":", ""), 16))
    known_numbers = FiniteSet(*(Integer(int(item.replace(":", ""), 16)) for item in TABLE))
    if mac_number not in known_numbers:
        raise ValueError("That MAC address is not in the sample table")
    return {"mac": mac, "ip": TABLE[mac]}


def client(data):
    return server(data)


def print_result(result):
    print(f"MAC address: {result['mac']}")
    print(f"Assigned IP: {result['ip']}")


def main():
    sample = {'mac': '02:00:5e:10:00:01'}
    print_result(client(sample))


if __name__ == "__main__":
    main()
