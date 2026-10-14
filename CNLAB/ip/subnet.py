
import simpy
import ipaddress

def server(env, channel):
    while True:
        ip = yield channel.get()
        print("Server received:", ip)
        net = ipaddress.ip_network(ip + "/24", strict=False)
        first = net.network_address + 1
        last = net.broadcast_address - 1
        yield env.timeout(2)
        result = "First usable IP: " + str(first) + "\nLast usable IP: " + str(last)
        print(result)

def client(env, channel):
    ip = "192.168.1.25"
    print("Client sending:", ip)
    yield channel.put(ip)
    yield env.timeout(3)
    print("Client received the result")

env = simpy.Environment()
channel = simpy.Store(env)
env.process(server(env, channel))
env.process(client(env, channel))
env.run()
