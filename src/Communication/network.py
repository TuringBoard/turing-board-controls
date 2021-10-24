'''
This file contains code that is will receive data packets from the Remote Control App
'''


import threading
import queue
import socket


class RemoteControl(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)

        # Used to store incoming data packets
        self.q = queue.Queue(255)
        self.lock = threading.Lock()

        self.s = None
        self.ip = ip
        self.port = port
        self.remote_control = None

    def __del__(self):
        self.s.close()

    def run(self):
        self.initalize_server()
        while True:
            self.command()

    def initalize_server(self):
        # IPv4, TCP Stream Socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen()
        print('Listening for incoming connection from remote...')
        self.remote_control, address = self.s.accept()
        print(f'Connected to {address}')

    def command(self):
        data = self.remote_control.recv(255)
        self.lock.acquire()
        if not self.q.full():
            self.q.put(data)
        self.lock.release()

    def poll(self):
        data = None
        self.lock.acquire()
        if not self.q.empty():
            data = self.q.get()
        self.lock.release()
        return data
