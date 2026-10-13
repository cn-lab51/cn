import json
import socket


HOST = "127.0.0.1"
PORT = 5501

def stuff(data):
    bits = data["bits"]
    group_size = int(data.get("group_size", 5))
    if not bits or any(bit not in "01" for bit in bits):
        raise ValueError("Enter a nonempty string containing only 0 and 1")
    if group_size < 1:
        raise ValueError("Group size must be positive")

    encoded = []
    ones = 0
    for bit in bits:
        encoded.append(bit)
        if bit == "1":
            ones += 1
            if ones == group_size:
                encoded.append("0")
                ones = 0
        else:
            ones = 0

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


def handle_client(connection):
    with connection:
        try:
            reader = connection.makefile("r", encoding="utf-8")
            request = json.loads(reader.readline())
            reply = {"ok": True, "result": stuff(request)}
        except (KeyError, TypeError, ValueError) as error:
            reply = {"ok": False, "error": str(error)}
        connection.sendall((json.dumps(reply) + "\n").encode("utf-8"))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Listening on {HOST}:{PORT}")
        while True:
            connection, _ = server.accept()
            handle_client(connection)


if __name__ == "__main__":
    main()
