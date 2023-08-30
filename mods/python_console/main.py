import threading
import code
import socket
import sys
from mods.python_console.config import port, host


class Stdio:
    def __init__(self):
        self.connection = None

    def set_connection(self, connection):
        self.connection = connection

    def write(self, mes):
        self.connection.send(mes.encode())

    def writeline(self, mes):
        self.connection.send((mes + "\n").encode())

    def read(self, *args, **kwargs):
        return self.connection.recv(1024).decode()

    def readline(self, *args, **kwargs):
        return self.connection.recv(1024).decode()

    def flush(self):
        pass


def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((host, port))
    stdio = Stdio()
    while True:
        s.listen()
        connection, _ = s.accept()
        stdio.set_connection(connection)

        sys.stderr = stdio

        sys.stdout = stdio

        sys.stdin = stdio
        try:
            code.interact(local=locals())
        except:
            pass


t = threading.Thread(target=start)
t.setDaemon(True)
t.start()
