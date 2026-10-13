# RARP lookup

## Files

- `server.py` runs a TCP server on `127.0.0.1:5502`.
- `client.py` connects to the server and prints the example result.
- `rarp_lookup_sympy.py` runs the same example locally using SymPy.

## Requirements

Python 3.9 or newer. The TCP files use only the standard library. Install SymPy for the standalone file with `python3 -m pip install --user sympy`. If your system blocks user installs, create a virtual environment with `python3 -m venv .venv`, activate it with `source .venv/bin/activate`, then run `python -m pip install sympy`.

## Run the TCP version

Open two terminals in this folder. In the first, run `python3 server.py` and leave it running. In the second, run `python3 client.py`. Edit the `request` value in `client.py` to try different input. Stop the server with Ctrl+C.

## Run the SymPy version

Run `python3 rarp_lookup_sympy.py`. It runs by itself and uses its built-in sample input.

## Example output

```text
MAC address: 02:00:5e:10:00:01
Assigned IP: 192.168.1.10
```

## Notes

The server looks up the supplied MAC address in a small sample RARP table. Add more MAC-to-IP pairs to TABLE to try other values. This is a local simulation, not a live LAN RARP service.
