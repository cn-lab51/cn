# CDMA chipping

## Files

- `server.py` runs a TCP server on `127.0.0.1:5504`.
- `client.py` connects to the server and prints the example result.
- `cdma_chipping_sympy.py` runs the same example locally using SymPy.

## Requirements

Python 3.9 or newer. The TCP files use only the standard library. Install SymPy for the standalone file with `python3 -m pip install --user sympy`. If your system blocks user installs, create a virtual environment with `python3 -m venv .venv`, activate it with `source .venv/bin/activate`, then run `python -m pip install sympy`.

## Run the TCP version

Open two terminals in this folder. In the first, run `python3 server.py` and leave it running. In the second, run `python3 client.py`. Edit the `request` value in `client.py` to try different input. Stop the server with Ctrl+C.

## Run the SymPy version

Run `python3 cdma_chipping_sympy.py`. It runs by itself and uses its built-in sample input.

## Example output

```text
Combined signal: [0, -2, 2, 0]
Client A recovered bit: 1
Client B recovered bit: -1
```

## Notes

Each client uses a +1 or -1 data bit and an equal-length chipping code. Codes must be orthogonal. The receiver adds the chip sequences, then correlates the sum with each client's code to recover its bit.
