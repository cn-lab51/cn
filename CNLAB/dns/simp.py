import simpy

def authoritative(env, domain):
    domains = {
        "example.com": "93.184.216.34",
        "google.com": "142.250.190.14"
    }

    print("Authoritative Server: Checking", domain)
    yield env.timeout(1)

    result = domains.get(domain, "Not Found")
    return result


def tld(env, domain):
    print("TLD Server: Forwarding to Authoritative Server")
    yield env.timeout(1)

    result = yield env.process(authoritative(env, domain))
    return result


def root(env, domain):
    print("Root Server: Forwarding to TLD Server")
    yield env.timeout(1)

    result = yield env.process(tld(env, domain))
    return result


def recursive(env, domain, client_id):
    print("\nClient", client_id, "requested:", domain)
    print("Recursive DNS: Contacting Root Server")

    result = yield env.process(root(env, domain))
    print("Client", client_id, "IP Address:", result)


def client(env, domain, client_id):
    yield env.timeout(0)
    yield env.process(recursive(env, domain, client_id))


env = simpy.Environment()

env.process(client(env, "google.com", 1))
env.process(client(env, "example.com", 2))
env.process(client(env, "unknown.com", 3))

env.run()