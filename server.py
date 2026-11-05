import os
import socket
import sys
import threading

HOST = sys.argv[1] if len(sys.argv) > 1 else "169.254.142.155"
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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        try:
            listener.bind((HOST, PORT))
        except OSError as error:
            print(f"Could not listen on {HOST}:{PORT}: {error}")
            print("Run ipconfig and check your Ethernet IP.")
            return

        listener.listen(1)
        print(f"Waiting for the other PC on {HOST}:{PORT}...", flush=True)
        conn, address = listener.accept()

    with conn:
        print(f"Connected to {address[0]}. Type /quit to exit.", flush=True)
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