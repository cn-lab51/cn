# Stop-and-Wait ARQ

## Files

- `server.py` runs a TCP server on `127.0.0.1:5503`.
- `client.py` connects to the server and prints the example result.
- `stop_and_wait_arq_sympy.py` runs the same example locally using SymPy.

## Requirements

Python 3.9 or newer. The TCP files use only the standard library. Install SymPy for the standalone file with `python3 -m pip install --user sympy`. If your system blocks user installs, create a virtual environment with `python3 -m venv .venv`, activate it with `source .venv/bin/activate`, then run `python -m pip install sympy`.

## Run the TCP version

Open two terminals in this folder. In the first, run `python3 server.py` and leave it running. In the second, run `python3 client.py`. Edit the `request` value in `client.py` to try different input. Stop the server with Ctrl+C.

## Run the SymPy version

Run `python3 stop_and_wait_arq_sympy.py`. It runs by itself and uses its built-in sample input.

## Example output

```text
Stop-and-Wait ARQ:
Send frame 0: Hello
ACK 0 received
Send frame 1: Network
ACK 1 lost; timeout
Retransmit frame 1: Network
ACK 1 received
Send frame 0: Lab
ACK 0 received
```

## Notes

The sender transmits one frame and waits for its ACK before sending the next. The sample drops the first ACK for frame 1 so you can see the timeout and retransmission. Sequence numbers alternate between 0 and 1.
