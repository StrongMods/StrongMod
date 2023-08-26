import code
import threading
from time import sleep

import api
from internal import game_controller
import code
import socket
import sys

def start():
    import code
    import socket
    import sys

    class Stdio():

        def __init__(self, sock_resp):
            self.sock_resp = sock_resp

        def write(self, mes):
            self.sock_resp.send(mes.encode())

        def readline(self):
            return self.sock_resp.recv(4096).decode()

    MY_IP = 'localhost'
    MY_PORT = 31337

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Start server")
    old_out = sys.stdout

    srv.bind((MY_IP, MY_PORT))
    srv.listen()
    sock_resp, addr_resp = srv.accept()
    stdio = Stdio(sock_resp)

    sys.stdout = stdio

    sys.stderr = stdio

    sys.stdin.read = stdio.readline
    sys.stdin.readline = stdio.readline

    code.interact(local=locals())
    print("close")

t = threading.Thread(target=start)
t.setDaemon(True)
t.start()
# code.interact(local=locals())
