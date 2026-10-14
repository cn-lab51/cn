# CNLAB computer networks programs

Clone the repository:

    git clone https://github.com/cn-lab51/cn.git
    cd cn/CNLAB

Each topic has its own folder. The TCP examples use Python's standard library. Start the server in one terminal, then start the client in another terminal from the same topic folder.

The files named simpy.py are simulations and need SimPy:

    python3 -m pip install --user simpy
    python3 bitstuffing/simpy.py

If your system blocks user-level pip installs, use a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install simpy

## Running the examples

- IP subnet: run server.py, then client.py in separate terminals in ip/.
- Bit stuffing: run server.py, then client.py in separate terminals in bitstuffing/.
- RARP: run server.py, then client.py in separate terminals in rarp/.
- Stop-and-Wait ARQ: run server.py, then client.py in separate terminals in stopandwaitarq/.
- CDMA: run server.py, then launch two client.py terminals, one for client A and one for client B, in cdma/.
- DNS: from dns/, start rootServer.py, comServer.py, exampleServer.py, arjunServer.py, localServer.py, then run client.py. Keep all server terminals open while testing.

The DNS example is configured for local connections at 127.0.0.1. These are lab simulations and use sample data.
