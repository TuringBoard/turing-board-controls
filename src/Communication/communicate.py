
'''
    Packet Structure: <Address><Data><Checksum>
'''

import threading
import queue
import serial
from enum import Enum


# This packet structure will be used for all communication of the Skateboard.
class Packet:
    def __init__(self):
        pass

    def add(self, data):
        pass


class SerialCommunication(threading.Thread):
    def __init__(self, port, baudrate, timeout=1):
        # The threading constructor needs to be overridden
        threading.Thread.__init__(self)

        # Buffer for receiving data
        self.rx_buffer = queue.Queue(255)
        self.rx_lock = threading.Lock()

        # Serial Communication intialization
        self.s = serial.Serial()
        self.s.port = port
        self.s.baudrate = baudrate
        self.s.timeout = timeout
        self.s.open()
    
    def __del__(self):
        if self.s.is_open():
            self.s.close()

    def run(self):
        self.receive()

    def receive(self):
        while True:
            rx_data = self.s.read(255)
            self.rx_lock.acquire()
            self.rx_buffer.put(rx_data)
            self.rx_lock.release()

    def poll(self):
        data = None
        self.rx_lock.acquire()
        if not self.rx_buffer.empty():
            data = self.rx_buffer.get()
        self.rx_lock.release()
        return data

    def send(self):
        pass
