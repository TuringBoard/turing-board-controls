# This file contains code that is will receive data packets from the Remote Control App


import threading
import queue


class RemoteControl(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.q = queue.Queue(1024)
        self.lock = threading.Lock()

    def __del__(self):
        pass

    def run(self):
        while True:
            self.command()

    def command(self):
        print("Enter: ", end="")
        i = input()
        self.lock.acquire()
        self.q.put(bytes(i, 'ascii'))
        self.lock.release()

    def poll(self):
        data = None
        self.lock.acquire()
        if not self.q.empty():
            data = self.q.get()
        self.lock.release()
        return data
