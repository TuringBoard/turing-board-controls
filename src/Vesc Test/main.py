from Communication.communicate import SerialCommunication
from Communication.network import RemoteControl
import numpy as np
import sys


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def main():
    s = SerialCommunication('COM9', 115200)
    print("Starting Serial Communication thread...")
    s.start()

    remote_control = RemoteControl()
    print("Starting Remote Control thread...")
    remote_control.initialize_network()

    # e is the exit flag
    e = False
    while not e:
        '''
        echo = s.poll()
        if echo:
            print(f"Echoed {echo}")
        '''
        speed = remote_control.poll()
        if speed:
            print(speed)
            speed = np.uint8(translate(speed, 0, 5, 0, 255))
            s.push(bytearray([speed]))
            s.send()

    s.join()


if __name__ == '__main__':
    main()
