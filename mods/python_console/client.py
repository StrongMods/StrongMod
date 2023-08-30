import functools
import socket
import threading

from mods.python_console.config import port, host

server_ip = host
server_port = port
# noinspection PyShadowingBuiltins
print = functools.partial(print, flush=True)


class Receiver:
    def __init__(self, s):
        self.s = s

    def receive(self):
        while True:
            try:
                data = self.s.recv(1024)
                print(data.decode(), end="")
            except OSError:
                break


while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        print(f"Connected to {server_ip}:{server_port}")
        receiver = Receiver(client_socket)
        threading.Thread(target=receiver.receive).start()

        while True:
            message = input("")
            if message == "":
                message = "\n"
            client_socket.send(message.encode())

    except (ConnectionRefusedError, OSError):
        print("Make sure the server is running.")
        if input("Retry?Y/n: ").lower() != "n":
            continue
        else:
            break

    except KeyboardInterrupt:
        client_socket.close()
        break
    finally:
        client_socket.close()
