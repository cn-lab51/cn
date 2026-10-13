# CDMA chipping, summation, and extraction

## Files

- `server.py` starts a TCP server on `127.0.0.1:5504`.
- `client.py` sends the example input to that server and prints a readable, labeled result (not JSON).
- `cdma_chipping_sympy.py` is an independent local implementation with `client()` and server-side calculation functions.

## Requirements

- Python 3.9 or newer.
- TCP client/server files use only the Python standard library.
- The standalone SymPy file requires SymPy. Install for your user account with `python3 -m pip install --user sympy`, or use an approved virtual environment: `python3 -m venv .venv`, then `source .venv/bin/activate` and `python -m pip install sympy`.

## Run the TCP version

Open two terminals in this folder. In terminal 1 run `python3 server.py`. In terminal 2 run `python3 client.py`. The client sends a built-in sample request and prints the server response. Edit the `request` value in `client.py` to try different input. Stop the server with Ctrl+C.

The server binds to localhost, so both terminals must be on the same machine. It does not need administrator access or a public network connection. If the port is already in use, change the same `PORT` value in both files.

## Run the SymPy version

Run `python3 cdma_chipping_sympy.py` in one terminal. It runs locally, without a server process, and prints a readable, labeled result for its built-in sample. Change the sample arguments in `main()` to try another input.

## Example output

```text
Composite signal: [0, -2, 2, 0]
Recovered data: A=1, B=-1
```

## Notes

Represent data bits as +1 or -1 and provide equal-length orthogonal chipping codes containing only +1 or -1. The receiver correlates the summed signal with each client code.
