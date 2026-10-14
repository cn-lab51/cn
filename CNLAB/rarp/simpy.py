
import simpy

table = {
    "AA:BB:CC:DD:EE:01": "192.168.1.10",
    "AA:BB:CC:DD:EE:02": "192.168.1.20",
    "AA:BB:CC:DD:EE:03": "192.168.1.30"
}

def server(env, requests):
    while True:
        mac = yield requests.get()
        print("Server received MAC:", mac)
        yield env.timeout(1)
        print("IP address:", table.get(mac, "MAC address not found"))

def client(env, requests):
    mac = "AA:BB:CC:DD:EE:01"
    print("Client sending MAC:", mac)
    yield requests.put(mac)

env = simpy.Environment()
requests = simpy.Store(env)
env.process(server(env, requests))
env.process(client(env, requests))
env.run(until=3)
