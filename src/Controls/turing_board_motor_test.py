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
speed_control_mutex = Lock()
# serial port that VESC is connected to. Something like "COM3" for windows and as below for linux/mac
serial_port = 'COM8'
remote_control_app = None
current_duty_cycle = 0.00
# Protected by a mutex. Stands for duty cycle truncated
current_duty_cycle_trunc = 0.00
autonomous_mode = False


def change_range(i, input_start, input_end, output_start, output_end):
    return output_start + ((output_end - output_start) / (input_end - input_start)) * (i - input_start)


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


def main():
    initialize_controls()
    run_wheels()


if __name__ == '__main__':
    main()
