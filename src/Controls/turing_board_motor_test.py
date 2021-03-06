'''
    Turning Board VESC Controls.
    Author: Runtime Terrors
'''

import atexit
from asyncio import locks, sleep
import sys, pyrebase, time
from threading import Lock
from config import *

'''
    Do not change these lines of code. It ensures that the pyvesc library is always found.
    The working principle is this: Go back a directory and include everything inside of dependecies.
    This way, this current module can find the pyvesc module.
'''
sys.path.insert(0, '../../dependencies/')
sys.path.insert(0, '../Communication')
sys.path.insert(0, '../../../turing-board-vision/arUcoTests')




from pyvesc import VESC                         # Controls the ESC
from communicate import SerialCommunication     # Establishes connection to the microcontroller
from arUcoDetectClass import FollowMe


def change_range(i, input_start, input_end, output_start, output_end):
    return output_start + ((output_end - output_start) / (input_end - input_start)) * (i - input_start)


class Controls:
    # def __init__(self, vesc_serial_port='/dev/ttyACM1', follow_me_serial_port='/dev/ttyACM0'):
    def __init__(self, vesc_serial_port='/dev/ttyACM1', follow_me_serial_port='/dev/ttyACM0'):
        # Serial port that VESC is connected to. Something like "COM3" for windows or '/dev/tty' for Linux
        self.turningMechanism = SerialCommunication(port=follow_me_serial_port, baudrate=115200)
        self.vesc_serial_port = vesc_serial_port
        self.follow_me_serial_port = follow_me_serial_port
        self.is_running = False
        self.autonomous_mode = False
        self.LEDMode = 3
        # This is a handle (Think of a literal handle) to the data stream
        # This will be used later to free up the resources used by the data stream
        self.remote_control_handler = None
        self.duty_cycle = 0
        # Mutex lock required as duty_cycle is being modified inside of two threads
        self.speed_control_mutex = Lock()
        self.max_speed = 5.00

        # Controls modules
        self.motor = None
        self.follow_me = None
        self.prevMode = 3

    # The destructor for the VESC call seems to be called automatically.
    # Leave this here as a contengency.
    # Make sure you clean up everything inside of the destructor.
    def __del__(self):
        if self.motor:
            del self.motor

    def initialize(self):
        # Intialize VESC
        print(f'Initializing Turning Board Controls ...\nUsing {self.vesc_serial_port}')
        self.motor = VESC(serial_port=self.vesc_serial_port, has_sensor=True)
        print('Initializing VESC...')
        # print(f'Firmware: {self.motor.get_firmware_version()}')
        # Intialize Follow Me Feature
        self.follow_me = FollowMe(self.follow_me_serial_port)

        # Intialize connection to the database
        # Create the database connection for receiving the speed values
        firebase = pyrebase.initialize_app(firebaseConfig)
        db = firebase.database()
        self.remote_control_handler = db.child(current_user).stream(self.__stream_handler)
        self.is_running = True

    # The diamter of the wheel = 3.5 in
    # Convert it to meter first and then divide by 2
    def __get_velocity(self, rpm):
        return round(((72 * 3.1415 * (0.0889/2)) / 965.6064)  * rpm, 2)

    # This private callback function is responsible for receiving data from the real-time database and processing it.
    # My best guess is that this function is run on a separate thread of execution.
    # @Keaton, @Happy, the double underscores make it a private function.
    def __stream_handler(self, speed):
        if self.is_running:
            # The call to the mutex should be okay as the speed argument already contains the data.
            # This means that a call to speed['data']['speed'] would never be blocking which is
            # important when it comes to a mutex as a block after a mutex is acquired would cause
            # a deadlock.
            self.speed_control_mutex.acquire()
            # Round the duty_cycle to 2 decimal places
            # The Duty Cycle that the ESC accepts ranges from 0 to 1
            # The mapping should be from the lower speed to the upper speed value which should be dynamic
            self.duty_cycle = round(change_range(speed['data']['speed'], 0.00, self.max_speed, 0.00, 0.99), 2)
            self.autonomous_mode = speed['data']['autonomous']
            self.LEDMode = speed['data']['mode']
            self.updateMode(speed['data']['mode'])
            self.speed_control_mutex.release()
    # red 0 
    # blue 1
    # green 2
    def updateMode(self, mode):
        if mode != self.prevMode:
            ledID = 2 & 0xFF
            ledMode = mode & 0xFF
            LEDData = [ledID, ledMode]
            LEDPacket = bytearray(LEDData)
            self.turningMechanism.push(LEDPacket)
            self.turningMechanism.send()
            if mode == 2:
                # self.follow_me.updateAngle(50) Ask happy
                self.updateLockState(0)            
            else:
                self.updateLockState(1)
        self.prevMode = mode
    
    def updateLockState(self, lock):
        lockID = 1 & 0xFF
        lockAngle = 50 & 0xFF # arbitrary
        lockDirection = 3 & 0xFF 
        lockState = lock & 0xFF
        lockData = [lockID, lockAngle, lockDirection, lockState]
        lockPacket = bytearray(lockData)
        self.turningMechanism.push(lockPacket)
        self.turningMechanism.send()

    def run(self):
        try:
            # Main loop
            while self.is_running:
                # time.sleep(0.1)
                if self.autonomous_mode == False:
                    self.speed_control_mutex.acquire()
                    self.motor.set_duty_cycle(-self.duty_cycle/10)
                    self.speed_control_mutex.release()
                else:
                    # Call CV follow-me code here
                    self.follow_me.follow_me(self.motor.set_duty_cycle, 0.035, 300)
                # print(f" RPM: {self.motor.get_rpm():>8} Velocity = {self.__get_velocity(self.motor.get_rpm()):>8} mph\r", end="")
        except KeyboardInterrupt:
            print('Exiting ...')
            self.is_running = False
            self.motor.set_duty_cycle(0)
            if self.remote_control_handler:
                self.remote_control_handler.close()
            self.follow_me.close_follow_me()


def main():
    # The maximum number of arguments required is 2
    # @Keaton, @Happy, this is a ternary operator. Mentioning it because the syntax
    # might be something you've not seen before.
    turning_board = Controls()
    turning_board.initialize()
    turning_board.run()
    atexit.register(turning_board.updateMode(3))

if __name__ == '__main__':
    main()

