# This file contains all API's required for communication between different modules of the Skateboard
# Each API needs to be non-blocking and would be called in a separate worker thread to send and receive data
# A receive and transmit queue will be used to make sure no data is being lost
'''
    Packet Structure: <Address><Data><Checksum>
'''
import threading
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
        self.rx_buffer = []
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
        while True:
            self.receive()

    def receive(self):
        self.rx_lock.acquire()
        self.rx_buffer.append(self.s.read(255))
        self.rx_lock.release()

    def poll(self):
        data = None
        self.rx_lock.acquire()
        if len(self.rx_buffer) > 0:
            data = self.rx_buffer.pop(0)
        self.rx_lock.release()
        return data

    def send(self):
        pass
