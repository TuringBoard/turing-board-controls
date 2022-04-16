from communicate import SerialCommunication
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


plt.subplots_adjust(bottom=0.35)

axis = plt.axes([0.20, 0.4, 0.65, 0.13])
 

  
def printName(name):
  print(name)
 


class RedBoardDataStructure:
  def __init__(self):
    # RGB values
    # self.led = [0, 0, 0]
    # # Direction, turning angle
    # self.turning = [68, 69]
    # self.solenoid = 0
    data = []

# X = 1,2, ...
# data = []
# print("before SerialCommunication init")
# usbmodem0E23569D1
# usbmodem0E22E54A1
# usbmodem0E228C441
turningMechanism = SerialCommunication(port="/dev/ttyACM0", baudrate=115200)
# print("before run")
# turningMechanism.run()

# print("before RedBoard init")
# dataToSend = RedBoardDataStructure()
# dataToSend.led = [66, 67, 68]
# dataToSend.turningMechanism = [69, 70]
# dataToSend.solenoid = 71

# This is the while loop inside the main controls code
# print(data)
# print("before Loop")
# while True:
#   turningMechanism.receive()
#   received = turningMechanism.poll()
#   print(received)
previous = 50
angle = Slider(axis, 'Angle', 0, 100, 50)
buttonAxis = plt.axes([0.81, 0.05, 0.1, 0.075])
homeBtn = Button(buttonAxis,'Home')

# def update(val):
#   global previous
#   a = int(angle.val)
#   angle1 = a
#   data.append(1 & 0xFF)  
#   data.append(int(angle1) & 0xFF)
#   direction = 0
#   if angle1 > previous:
#     direction = 1
#   data.append(int(direction) & 0xFF)
#   rate = 0
#   data.append(int(rate) & 0xFF)
#   print("data:",data)
#   toSend = bytearray(data)
#   print("bytearray:", toSend)
#   turningMechanism.push(toSend)
#   turningMechanism.send()
#   previous = angle1
#   del data[:]

# def goHome(e):
#   global previous
#   a = 50
#   angle1 = a
#   data.append(1 & 0xFF)  
#   data.append(int(angle1) & 0xFF)
#   direction = 2
#   data.append(int(direction) & 0xFF)
#   rate = 0
#   data.append(int(rate) & 0xFF)
#   print("data:",data)
#   toSend = bytearray(data)
#   print("bytearray:", toSend)
#   turningMechanism.push(toSend)
#   turningMechanism.send()
#   previous = angle1
# #   del data[:]
  
# def updateAngle(angle1): 
#   print("update command sent", angle1)
#   global previous
#   data = []
#   data.append(1 & 0xFF)  
#   data.append(int(angle1) & 0xFF)
#   direction = 0
#   if angle1 > previous:
#     direction = 1
#   data.append(int(direction) & 0xFF)
#   rate = 0
#   data.append(int(rate) & 0xFF)
#   print("data:",data)
#   toSend = bytearray(data)
#   print("bytearray:", toSend)
#   turningMechanism.push(toSend)
#   print("b4", toSend)
#   turningMechanism.send()
#   print("after")
#   previous = angle1

# angle.on_changed(update)

# homeBtn.on_clicked(goHome)

# def helperFn(angle2):
  # updateAngle(int(angle2))

# while True: 
#   angle2 = int(input("Enter angle: "))
#   updateAngle(angle2)
    
# plt.show()

# while True:
  
  # turningMechanism.receive()
  # received = bytearray(turningMechanism.poll())
  # print("received data")
  # print(received)
  # Receive input here
  # id = 2
  # mode = int(input("Enter mode: "))
  # data = []
  # data.append(id & 0xFF)
  # data.append(mode & 0XFF)
  # turningMechanism.push(data)
  # turningMechanism.send()
  # del data[:]
  
  
#     # Convert dataToSend to an array of uint8_t's
  
#   print("data: ")
#   print(data)
#   # dataToSend = bytes(dataToSend)
#   toSend = bytearray(data)
#   print("byte array: ")
#   print(toSend)
#   # This is to send data
#   turningMechanism.push(toSend)
#   print("before sending")
#   turningMechanism.send()
#   # print("before receiving")
#   turningMechanism.receive()
#   print("before polling")
#   received = []
#   while not received:
#     received = bytearray(turningMechanism.poll())
#   print("received data")
#   print(received)
#   # print(received[1])
#   # del received[:]
#   del data[:]
