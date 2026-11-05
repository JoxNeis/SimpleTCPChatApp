import os
import socket
import sys
import threading

SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else "169.254.142.155"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5000


def receive_messages(conn):
    """Print incoming messages until the connection closes."""
    try:
        with conn.makefile("r", encoding="utf-8", newline="\n") as messages:
            for message in messages:
                print(f"\rOther PC: {message.rstrip()}\nYou: ", end="", flush=True)
    except OSError:
        pass

    print("\nDisconnected.", flush=True)
    os._exit(0)


def main():
    print(f"Connecting to {SERVER_IP}:{PORT}...", flush=True)

    try:
        conn = socket.create_connection((SERVER_IP, PORT), timeout=10)
    except OSError as error:
        print(f"Could not connect: {error}")
        print("Check that chat_server.py is running and the IP is correct.")
        return

    conn.settimeout(None)

    with conn:
        print("Connected. Type /quit to exit.", flush=True)
        threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

        while True:
            try:
                message = input("You: ")
            except (EOFError, KeyboardInterrupt):
                break

            if message == "/quit":
                break

            try:
                conn.sendall((message + "\n").encode("utf-8"))
            except OSError:
                print("Could not send the message.")
                break


if __name__ == "__main__":
    main()