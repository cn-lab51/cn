from sympy import Integer

def server(data):
    bits = data["bits"]
    group_size = int(data.get("group_size", 5))
    if not bits or any(bit not in "01" for bit in bits):
        raise ValueError("Enter a nonempty string containing only 0 and 1")
    if group_size < 1:
        raise ValueError("Group size must be positive")

    encoded = []
    ones = Integer(0)
    for bit in bits:
        encoded.append(bit)
        if bit == "1":
            ones += 1
            if ones == group_size:
                encoded.append("0")
                ones = Integer(0)
        else:
            ones = Integer(0)

    stuffed = "".join(encoded)
    return {"original": bits, "stuffed": stuffed, "removed": destuff(stuffed, group_size)}


def destuff(bits, group_size):
    result = []
    ones = 0
    index = 0
    while index < len(bits):
        bit = bits[index]
        result.append(bit)
        if bit == "1":
            ones += 1
            if ones == group_size:
                index += 1
                if index == len(bits) or bits[index] != "0":
                    raise ValueError("Expected a stuffed zero")
                ones = 0
        else:
            ones = 0
        index += 1
    return "".join(result)


def client(data):
    return server(data)


def print_result(result):
    print(f"Original bits: {result['original']}")
    print(f"Stuffed bits:  {result['stuffed']}")
    print(f"After removal: {result['removed']}")


def main():
    sample = {'bits': '1111101111110', 'group_size': 5}
    print_result(client(sample))


if __name__ == "__main__":
    main()
