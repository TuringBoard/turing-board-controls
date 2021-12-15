'''
    Turning Board VESC Controls.
    Author: Runtime Terrors
'''

import sys, pyrebase
from enum import IntEnum
from threading import Lock
from config import *

'''
    Do not change these lines of code. It ensures that the pyvesc library is always found.
    The working principle is this: Go back a directory and include everything inside of dependecies.
    This way, this current module can find the pyvesc module.
'''
sys.path.insert(0, '../../dependencies/')
sys.path.insert(0, '../Communication')

from pyvesc import VESC                         # Controls the ESC
from communicate import SerialCommunication     # Establishes connection to the microcontroller


def change_range(i, input_start, input_end, output_start, output_end):
    return output_start + ((output_end - output_start) / (input_end - input_start)) * (i - input_start)


class TurningBoardState(IntEnum):
    STOP = 0


class Controls:
    def __init__(self, serial_port_name='COM8'):
        # Serial port that VESC is connected to. Something like "COM3" for windows or '/dev/tty' for Linux
        self.serial_port_name = serial_port_name
        self.is_runnig = False
        self.autonomous_mode = False
        # This is a handle (Think of a literal handle) to the data stream
        # This will be used later to free up the resources used by the data stream
        self.remote_control_handler = None
        self.duty_cycle = 0
        # Mutex lock required as duty_cycle is being modified inside of two threads
        self.speed_control_mutex = Lock()
        self.max_speed = 5.00

        self.motor = None

    # The destructor for the VESC call seems to be called automatically.
    # Leave this here as a contengency.
    # Make sure you clean up everything inside of the destructor.
    def __del__(self):
        if self.motor:
            del self.motor
        
        if self.remote_control_handler:
            self.remote_control_handler.close()

    def initialize(self):
        print(f'Initializing Turning Board Controls ...\nUsing {self.serial_port_name}')
        self.motor = VESC(serial_port=self.serial_port_name, has_sensor=True)
        print(f'Firmware: {self.motor.get_firmware_version()}')
        # Create the database connection for receiving the speed values
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        self.remote_control_handler = db.child(current_user).stream(self.__stream_handler)
        self.is_runnig = True

    # This private callback function is responsible for receiving data from the real-time database and processing it.
    # My best guess is that this function is run on a separate thread of execution.
    # @Keaton, @Happy, the double underscores make it a private function.
    def __stream_handler(self, speed):
        if self.is_runnig:
            # The call to the mutex should be okay as the speed argument already contains the data.
            # This means that a call to speed['data']['speed'] would never be blocking which is
            # important when it comes to a mutex as a block after a mutex is acquired would cause
            # a deadlock.
            self.speed_control_mutex.acquire()
            # Round the duty_cycle to 2 decimal places
            # The Duty Cycle that the ESC accepts ranges from 0 to 1
            # The mapping should be from the lower speed to the upper speed value which should be dynamic
            self.duty_cycle = round(change_range(speed['data']['speed'], 0.00, self.max_speed, 0.00, 0.99), 2)
            self.speed_control_mutex.release()

    def run(self):
        try:
            while self.is_runnig:
                if not self.autonomous_mode:
                    self.speed_control_mutex.acquire()
                    self.motor.set_duty_cycle(self.duty_cycle)
                    self.speed_control_mutex.release()
                else:
                    # Call CV follow-me code here
                    pass
                print(f"RPM: {self.motor.get_rpm():8}\r", end="")
        except KeyboardInterrupt:
            print('Exiting ...')
            self.is_runnig = False
            self.motor.set_duty_cycle(0)


def main():
    # initialize_controls()
    # run_wheels()
    # The maximum number of arguments required is 2
    # @Keaton, @Happy, this is a ternary operator
    turning_board = Controls(sys.argv[1]) if len(sys.argv) == 2 else Controls()
    turning_board.initialize()
    turning_board.run()


if __name__ == '__main__':
    main()
