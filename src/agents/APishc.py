import socket
import argparse
import sys
from time import sleep


BUFFER_SIZE = 4096


def write(data, stderr=False):
    """
    Print without newline. If stderr is True print to sys.stderr
    instead to sys.stdout.
    """
    if stderr:
        print(data, file=sys.stderr, end="")
    else:
        print(data, end="")


def stdin(host, port):
    """
    Send to agent's stdin via socket on ( host, port ). Works
    as a shell.
    """
    s = socket.socket()
    s.connect((host, port))
    s.settimeout(0.1)
    while True:
        try:
            res = s.recv(BUFFER_SIZE).decode()
            write(res, False)
            if "Input end delimiter received, agent is shutting down..." in res:
                s.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
                s.close()
                break
            inp = input()
            if inp == "exit":
                s.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
                s.close()
                break
            s.send(inp.encode())
        except Exception as e:
            if e.errno == 107:  # Agent disconnected
                print("Error, agent has disconnected!")
                break


def out(host, port, write_error=False):
    """
    Write data from agent's stdout via socket on ( host, port ).
    If write_error is True, write to sys.stderr instead of sys.stdout.
    """
    s = socket.socket()
    s.connect((host, port))
    s.settimeout(0.1)
    last_res = ""
    while True:
        try:
            res = s.recv(BUFFER_SIZE).decode()
            write(res, write_error)
            if res:
                last_res = res
            if "Output end delimiter received, agent is shutting down..." in last_res:
                s.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
                s.close()
                break
        except Exception as e:
            sleep(0.1)
            print(e)
            print(e.errno)
            if e.errno == 107:  # Agent disconnected
                print("Error, agent has disconnected!")
                break


def main(host, port, provide_input=True, write_output=True, write_error=False):
    """
    Main client's function. Start appropriate function based on
    given input params.
    host - agent's socket host
    port - agent's socket port
    provide_input - if True start input shell (write_output and write_error will be ignored)
    write_output - if True write agent's output to stdout (write_error will be ignored)
    write_error - if True write agent's output to stderr
    """
    if provide_input:
        stdin(host, port)
    elif write_output:
        out(host, port)
    elif write_error:
        out(host, port, True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="APi shell client: connect to any stdin/stdout/stderr listening/writing agent."
    )
    parser.add_argument("host", metavar="HOST", type=str, help="Agent's host")
    parser.add_argument("port", metavar="PORT", type=int, help="Agent's port")
    parser.add_argument(
        "--input",
        action="store_true",
        help="If provided input can be sent to agent. The other arguments (output, error) will be ignored.",
    )
    parser.add_argument(
        "--output",
        action="store_true",
        help="If provided agent's output will be written to stdout. Argument error will be ignored. ",
    )
    parser.add_argument(
        "--error",
        action="store_true",
        help="If provided agent's output will be written to stderr.",
    )

    args = parser.parse_args()
    main(args.host, args.port, args.input, args.output, args.error)
