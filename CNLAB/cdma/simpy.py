
import simpy

codes = {
    "A": [1, 1, 1, 1],
    "B": [1, -1, 1, -1]
}

def server(env, requests):
    data = {}
    for i in range(2):
        name, bit = yield requests.get()
        data[name] = 1 if bit == "1" else -1
        print("Server received from", name, ":", bit)

    signal = [
        data["A"] * codes["A"][i] + data["B"] * codes["B"][i]
        for i in range(4)
    ]
    print("Combined signal:", signal)

    for name in codes:
        value = sum(signal[i] * codes[name][i] for i in range(4)) // 4
        print("Decoded", name + ":", 1 if value > 0 else 0)

def client(env, requests, name, bit):
    print("Client", name, "sending:", bit)
    yield requests.put((name, bit))

env = simpy.Environment()
requests = simpy.Store(env)
env.process(server(env, requests))
env.process(client(env, requests, "A", "1"))
env.process(client(env, requests, "B", "0"))
env.run(until=2)
