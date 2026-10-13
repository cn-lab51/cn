# Recursive DNS

## Files

- `server.py` runs a TCP server on `127.0.0.1:5505`.
- `client.py` connects to the server and prints the example result.
- `recursive_dns_sympy.py` runs the same example locally using SymPy.

## Requirements

Python 3.9 or newer. The TCP files use only the standard library. Install SymPy for the standalone file with `python3 -m pip install --user sympy`. If your system blocks user installs, create a virtual environment with `python3 -m venv .venv`, activate it with `source .venv/bin/activate`, then run `python -m pip install sympy`.

## Run the TCP version

Open two terminals in this folder. In the first, run `python3 server.py` and leave it running. In the second, run `python3 client.py`. Edit the `request` value in `client.py` to try different input. Stop the server with Ctrl+C.

## Run the SymPy version

Run `python3 recursive_dns_sympy.py`. It runs by itself and uses its built-in sample input.

## Example output

```text
Recursive DNS lookup:
Client asks the recursive resolver
Resolver asks a root server
Root server points to the .com TLD server
TLD server points to the example.com authoritative server
Authoritative server returns the address
Resolver returns the answer to the client
Answer: www.example.com -> 93.184.216.34
```

## Notes

This example uses a small local DNS table and prints the recursive lookup path through the root, TLD, and authoritative servers. It simulates the lookup; it does not contact public DNS servers. Add names to RECORDS to try other inputs.
