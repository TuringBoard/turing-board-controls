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

        # IPv4, TCP Stream Socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'Trying to establish connection to {ip}:{port}')
        self.s.connect((ip, port))
        print(f'Connected to {ip}:{port}')

    def __del__(self):
        self.s.close()

    def run(self):
        while True:
            self.command()

    def command(self):
        data = self.s.recv(255)
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
