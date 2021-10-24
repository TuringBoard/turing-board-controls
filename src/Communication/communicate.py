'''
    Packet Structure: <Address><Data><Checksum>
'''

import threading
import queue
import serial

# This packet structure will be used for all communication of the Skateboard.
class Packet:
    def __init__(self):
        pass

    def add(self, data):
        pass


class ReceiveThread(threading.Thread):
    def __init__(self, port, baudrate, timeout=1):
        # The threading constructor needs to be overridden
        threading.Thread.__init__(self)

        # The architecture uses an RX and TX buffer for data transmission
        # Buffer for receiving data
        # Buffer for sending data
        self.rx_buffer = queue.Queue(255)
        self.tx_buffer = queue.Queue(255)
        self.transmit_lock = threading.Lock()

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
            self.transmit_lock.acquire()
            self.rx_buffer.put(rx_data)
            self.transmit_lock.release()

    # Used to check if the receive buffer has any data or not
    def poll(self):
        data = None
        self.transmit_lock.acquire()
        if not self.rx_buffer.empty():
            data = self.rx_buffer.get()
        self.transmit_lock.release()
        return data

    # This might be a potential place for a deadlock
    def send(self):
        self.transmit_lock.acquire()
        if not self.tx_buffer.empty():
            data = self.tx_buffer.get()
            self.s.write(data)
            self.s.flush()
        self.transmit_lock.release()

    # Used to queue up data to send
    def push(self, data):
        self.transmit_lock.acquire()
        self.tx_buffer.put(data)
        self.transmit_lock.release()
