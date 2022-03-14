from communicate import SerialCommunication
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


plt.subplots_adjust(bottom=0.35)

axis = plt.axes([0.20, 0.4, 0.65, 0.13])
 

  

 


class RedBoardDataStructure:
  def __init__(self):
    # RGB values
    # self.led = [0, 0, 0]
    # # Direction, turning angle
    # self.turning = [68, 69]
    # self.solenoid = 0
    data = []

# X = 1,2, ...
data = []
print("before SerialCommunication init")
# usbmodem0E23569D1
# usbmodem0E22E54A1
turningMechanism = SerialCommunication("/dev/ttyACM0", 115200)
print("before run")
# turningMechanism.run()

print("before RedBoard init")
# dataToSend = RedBoardDataStructure()
# dataToSend.led = [66, 67, 68]
# dataToSend.turningMechanism = [69, 70]
# dataToSend.solenoid = 71

# This is the while loop inside the main controls code
print(data)
print("before Loop")
# while True:
#   turningMechanism.receive()
#   received = turningMechanism.poll()
#   print(received)
angle = Slider(axis, 'Angle', 0, 90, 45)
def update(val):
  a = int(angle.val)
  angle1 = a
  data.append(1 & 0xFF)  
  data.append(int(angle1) & 0xFF)
  direction = 0
  if angle1 > 45:
    direction = 1
  data.append(int(direction) & 0xFF)
  rate = 0
  data.append(int(rate) & 0xFF)
  print("data:",data)
  toSend = bytearray(data)
  print("bytearray:", toSend)
  turningMechanism.push(toSend)
  turningMechanism.send()
  del data[:]

angle.on_changed(update)

  
    
plt.show()

# while True:
  
#   # turningMechanism.receive()
#   # received = bytearray(turningMechanism.poll())
#   # print("received data")
#   # print(received)
#   # Receive input here
#   print("Enter ID: ")
#   id = input()
  
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

