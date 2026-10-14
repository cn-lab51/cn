import simpy
def server(env, frames, acks):
    while True:
        seq, data = yield frames.get()
        print("Server received:", data)
        yield env.timeout(1)
        yield acks.put(seq)
        print("Server sent ACK:", seq)
def client(env, frames, acks):
    data_list = ["Hello", "Computer", "Networks", "Done"]
    for i, data in enumerate(data_list):
        seq = i % 2
        print("Client sending:", data)
        yield frames.put((seq, data))
        ack = yield acks.get()
        print("Client received ACK:", ack)
        yield env.timeout(0.5)
env = simpy.Environment()
frames = simpy.Store(env)
acks = simpy.Store(env)
env.process(server(env, frames, acks))
env.process(client(env, frames, acks))
env.run(until=10)
