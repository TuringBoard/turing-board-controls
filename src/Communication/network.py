# This file is no longer required

'''
Turing Board RCA v0.1

This file contains code that is will receive data packets from the Remote Control App (RCA).

This class creates a separate thread dedicated to receiving a connection from the RCA.
Once a connection has been established, data can be sent easily from the RCA which will be
forwarded to the micro controller.
'''


import threading
import queue
import socket
import pyrebase


firebaseConfig = {
    "apiKey": "AIzaSyDNS6tW71-jOsGKOGrh6V5dQWTfZSS6tCI",
    "databaseURL": "https://turing-board-default-rtdb.firebaseio.com/",
    "authDomain": "turing-board.firebaseapp.com",
    "projectId": "turing-board",
    "storageBucket": "turing-board.appspot.com",
    "messagingSenderId": "1008426809841",
    "appId": "1:1008426809841:web:0e490af3b6046f64aeec50"
}


'''
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
            pass

    def initalize_server(self):
        # IPv4, TCP Stream Socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.ip, self.port))
        self.s.listen()
        print('Listening for incoming connection from remote...')
        self.remote_control, address = self.s.accept()
        print(f'Connected to {address}')

    def command(self, message):
        # data = self.remote_control.recv(255)
        # print(message["data"])
        self.lock.acquire()
        if not self.q.full():
            self.q.put(message["data"]['speed'])
        self.lock.release()

    def poll(self):
        data = None
        self.lock.acquire()
        if not self.q.empty():
            data = self.q.get()
        self.lock.release()
        return data
'''


class RemoteControl:
    def __init__(self):

        # Used to store incoming data packets
        self.q = queue.Queue(255)
        self.lock = threading.Lock()

        self.firebase = pyrebase.initialize_app(firebaseConfig)
        self.db = self.firebase.database()

    def __del__(self):
        pass

    def command(self, message):
        self.lock.acquire()
        if not self.q.full():
            self.q.put(message["data"]['speed'])
        self.lock.release()

    def initialize_network(self):
        self.db.child("users/VR8SIRfZHNdo9mTTMENnf1tZQd52").stream(self.command)

    def poll(self):
        data = None
        self.lock.acquire()
        if not self.q.empty():
            data = self.q.get()
        self.lock.release()
        return data
