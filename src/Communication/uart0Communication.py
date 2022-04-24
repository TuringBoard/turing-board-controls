from communicate import SerialCommunication
import time

turningMechanism = SerialCommunication(port="/dev/ttyACM0", baudrate=115200)
