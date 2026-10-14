
import simpy

def server(env, channel):
    while True:
        bits = yield channel.get()
        print("Server received:", bits)
        stuffed = ""
        count = 0
        for bit in bits:
            stuffed += bit
            if bit == "1":
                count += 1
                if count == 5:
                    stuffed += "0"
                    count = 0
            else:
                count = 0
        yield env.timeout(1)
        original = ""
        count = 0
        i = 0
        while i < len(stuffed):
            bit = stuffed[i]
            original += bit
            if bit == "1":
                count += 1
                if count == 5:
                    i += 1
                    count = 0
            else:
                count = 0
            i += 1
        print("Stuffed:", stuffed)
        print("Destuffed:", original)

def client(env, channel):
    bits = "111110111111"
    print("Client sending:", bits)
    yield channel.put(bits)

env = simpy.Environment()
channel = simpy.Store(env)
env.process(server(env, channel))
env.process(client(env, channel))
env.run(until=3)
