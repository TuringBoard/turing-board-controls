'''
    Turning Board VESC Controls.
    Author: Dumb Truck Boyz
'''

import sys, time, pyrebase
from threading import Lock
from config import *

'''
    Do not change this line of code. It ensures that the pyvesc library is always found.
    The working principle is this: Go back a directory and include everything inside of dependecies.
    This way, this current module can find the pyvesc module.
'''
sys.path.insert(0, '../../dependencies/')

from pyvesc import VESC


'''
    Mutex lock required as current_duty_cycle_trunc is being modified inside of two threads
'''

'''
speed_control_mutex = Lock()
# serial port that VESC is connected to. Something like "COM3" for windows and as below for linux/mac
serial_port = 'COM8'
remote_control_app = None
current_duty_cycle = 0.00
# Protected by a mutex. Stands for duty cycle truncated
current_duty_cycle_trunc = 0.00
autonomous_mode = False


# This callback is responsible for receiving data from the real-time database and processing it
def stream_handler(speed):
    # This is required to reference the global variable current_duty_cycle_trunc
    global current_duty_cycle_trunc
    current_duty_cycle = change_range(float(speed['data']['speed']), 0.00, 5.00, 0.00, 0.99)
    speed_control_mutex.acquire()
    # The duty cycle is correct to 2 decimal place
    current_duty_cycle_trunc = float(str(current_duty_cycle)[0:3])
    speed_control_mutex.release()
    # print(current_duty_cycle_trunc)


def initialize_controls():
    global remote_control_app
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    remote_control_app = db.child(current_user).stream(stream_handler)


def run_wheels():
    with VESC(serial_port=serial_port, has_sensor=True) as motor:
        print("Firmware: ", motor.get_firmware_version())
        print(f"Input voltage (V): {motor.get_v_in()}")

        try:
            # This will be the main loop of the controls code
            while True:
                if not autonomous_mode:
                    speed_control_mutex.acquire()
                    motor.set_duty_cycle(current_duty_cycle_trunc)
                    speed_control_mutex.release()
                else:
                    # Call CV follow-me code here
                    pass
                print(f"RPM: {motor.get_rpm():8}\r", end="")
        except KeyboardInterrupt:
            # Close all connections
            motor.set_duty_cycle(0)
            remote_control_app.close()
'''


def change_range(i, input_start, input_end, output_start, output_end):
    return output_start + ((output_end - output_start) / (input_end - input_start)) * (i - input_start)


class Controls:
    def __init__(self, serial_port_name='COM8'):
        # Serial port that VESC is connected to. Something like "COM3" for windows or '/dev/tty' for Linux
        self.serial_port_name = serial_port_name
        self.autonomous_mode = False
        # This is a handle (Think of a literal handle) to the data stream
        # This will be used later to free up the resources used by the data stream
        self.remote_control_handler = None
        self.duty_cycle = 0
        # Mutex lock required as duty_cycle is being modified inside of two threads
        self.speed_control_mutex = Lock()

        self.motor = None

    # The destructor for the VESC call seems to be called automatically.
    # Leave this here as a contengency.
    # Make sure you clean up everything inside of the destructor.
    def __del__(self):
        if self.motor:
            del self.motor

    def initialize(self):
        print('Initializing Turning Board Controls ...')
        self.motor = VESC(serial_port=self.serial_port_name, has_sensor=True)
        print(f'Firmware: {self.motor.get_firmware_version()}')
        # Create the database connection for receiving the speed values
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        self.remote_control_handler = db.child(current_user).stream(self.__stream_handler)

    # This private callback function is responsible for receiving data from the real-time database and processing it.
    # My best guess is that this function is run on a separate thread of execution.
    # @Keaton, @Happy, the double underscores make it a private function.
    def __stream_handler(self, speed):
        # The call to the mutex should be okay as the speed argument already contains the data.
        # This means that a call to speed['data']['speed'] would never be blocking which is
        # important when it comes to a mutex as a block after a mutex is acquired would cause
        # a deadlock.
        self.speed_control_mutex.acquire()
        # Round the duty_cycle to 2 decimal places
        self.duty_cycle = round(change_range(speed['data']['speed'], 0.00, 5.00, 0.00, 0.99), 2)
        self.speed_control_mutex.release()

    def run(self):
        try:
            while True:
                if not self.autonomous_mode:
                    self.speed_control_mutex.acquire()
                    self.motor.set_duty_cycle(self.duty_cycle)
                    self.speed_control_mutex.release()
                else:
                    # Call CV follow-me code here
                    pass
                print(f"RPM: {self.motor.get_rpm():8}\r", end="")
        except KeyboardInterrupt:
            # Close all connections
            self.motor.set_duty_cycle(0)
            self.remote_control_handler.close()


def main():
    # initialize_controls()
    # run_wheels()
    turning_board = Controls()
    turning_board.initialize()
    turning_board.run()


if __name__ == '__main__':
    main()
