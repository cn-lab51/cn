# Subnetting

## Files

- `server.py` runs a TCP server on `127.0.0.1:5500`.
- `client.py` connects to the server and prints the example result.
- `subnetting_sympy.py` runs the same example locally using SymPy.

## Requirements

Python 3.9 or newer. The TCP files use only the standard library. Install SymPy for the standalone file with `python3 -m pip install --user sympy`. If your system blocks user installs, create a virtual environment with `python3 -m venv .venv`, activate it with `source .venv/bin/activate`, then run `python -m pip install sympy`.

## Run the TCP version

Open two terminals in this folder. In the first, run `python3 server.py` and leave it running. In the second, run `python3 client.py`. Edit the `request` value in `client.py` to try different input. Stop the server with Ctrl+C.

## Run the SymPy version

Run `python3 subnetting_sympy.py`. It runs by itself and uses its built-in sample input.

## Example output

```text
Network: 192.168.1.0/24
First usable IP: 192.168.1.1
Last usable IP: 192.168.1.254
Broadcast address: 192.168.1.255
```

## Notes

Enter an IPv4 address and prefix. This example uses /24 by default and reports the network, first and last usable addresses, and broadcast address. Prefixes /31 and /32 are excluded because they do not have conventional network and broadcast host ranges.
