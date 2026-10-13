from sympy import Matrix

def server(data):
    clients = data["clients"]
    names = list(clients)
    if not names:
        raise ValueError("Add at least one client")

    size = len(clients[names[0]]["code"])
    signal = Matrix([0] * size)
    codes = {}
    for name, client in clients.items():
        code = client["code"]
        bit = client["bit"]
        if len(code) != size or bit not in (-1, 1):
            raise ValueError("Use equal-length codes and data bits of 1 or -1")
        if any(chip not in (-1, 1) for chip in code):
            raise ValueError("Each chip must be 1 or -1")
        codes[name] = Matrix(code)
        signal += bit * codes[name]

    recovered = {}
    for name, code in codes.items():
        for other_name, other in codes.items():
            if name != other_name and (code.dot(other) != 0):
                raise ValueError("Client codes must be orthogonal")
        score = code.dot(signal)
        recovered[name] = 1 if score > 0 else -1 if score < 0 else 0

    return {"signal": list(signal), "recovered": recovered}


def client(data):
    return server(data)


def print_result(result):
    print(f"Combined signal: {result['signal']}")
    for name, bit in result["recovered"].items():
        print(f"Client {name} recovered bit: {bit}")


def main():
    sample = {'clients': {'A': {'bit': 1, 'code': [1, -1, 1, -1]}, 'B': {'bit': -1, 'code': [1, 1, -1, -1]}}}
    print_result(client(sample))


if __name__ == "__main__":
    main()
