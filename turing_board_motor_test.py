'''
    Turning Board VESC Controls
'''

from pyvesc import VESC
import time
import pyrebase
from threading import Lock


# serial port that VESC is connected to. Something like "COM3" for windows and as below for linux/mac
serial_port = 'COM8'
current_duty_cycle = 0.00
current_duty_cycle_trunc = 0.00
'''
    Mutex lock required as current_duty_cycle_trunc is being modified inside of two threads
'''
speed_mutex = Lock()


firebaseConfig = {
    "apiKey": "AIzaSyDNS6tW71-jOsGKOGrh6V5dQWTfZSS6tCI",
    "databaseURL": "https://turing-board-default-rtdb.firebaseio.com/",
    "authDomain": "turing-board.firebaseapp.com",
    "projectId": "turing-board",
    "storageBucket": "turing-board.appspot.com",
    "messagingSenderId": "1008426809841",
    "appId": "1:1008426809841:web:0e490af3b6046f64aeec50"
}


firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


def change_range(i, input_start, input_end, output_start, output_end):
    return output_start + ((output_end - output_start) / (input_end - input_start)) * (i - input_start)


def stream_handler(speed):
    global current_duty_cycle_trunc
    current_duty_cycle = change_range(float(speed['data']['speed']), 0.00, 5.00, 0.00, 0.99)
    speed_mutex.acquire()
    # The duty cycle is correct to 2 decimal place
    current_duty_cycle_trunc = float(str(current_duty_cycle)[0:3])
    speed_mutex.release()
    # print(current_duty_cycle_trunc)


db.child("users/gXcA4yBykAS05reLm4guWoIn8D12").stream(stream_handler)


def run_motor_using_user_input():
    with VESC(serial_port=serial_port) as motor:
        print("Firmware: ", motor.get_firmware_version())
        
        try:
            while True:
                time.sleep(0.1)
                speed_mutex.acquire()
                motor.set_duty_cycle(current_duty_cycle_trunc)
                speed_mutex.release()
        except KeyboardInterrupt:
            motor.set_rpm(0)


if __name__ == '__main__':
    run_motor_using_user_input()
