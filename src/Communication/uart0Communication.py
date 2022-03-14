from communicate import SerialCommunication
import time

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
turningMechanism = SerialCommunication("/dev/cu.usbmodem0E22E54A1", 115200)
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

while True:
  # turningMechanism.receive()
  # received = bytearray(turningMechanism.poll())
  # print("received data")
  # print(received)
  # Receive input here
  print("Enter ID: ")
  id = input()
  data.append(int(id) & 0xFF)
  if id == 1:
    print("Enter angle: ")
    angle = input()
    data.append(int(angle) & 0xFF)
    print("\nEnter direction: ")
    direction = input()
    data.append(int(direction) & 0xFF)
    print("\nEnter Rate: ")
    rate = input()
    data.append(int(rate) & 0xFF)
    # Convert dataToSend to an array of uint8_t's
  if id == 2:
    print("Enter Color: ")
    color = input()
    data.append(int(color) & 0XFF)
    data.append(int(0))
    data.append(int(0))
  print("data: ")
  print(data)
  # dataToSend = bytes(dataToSend)
  toSend = bytearray(data)
  print("byte array: ")
  print(toSend)
  # This is to send data
  turningMechanism.push(toSend)
  print("before sending")
  turningMechanism.send()
  # print("before receiving")
  turningMechanism.receive()
  print("before polling")
  received = []
  while not received:
    received = bytearray(turningMechanism.poll())
  print("received data")
  print(received)
  # print(received[1])
  # del received[:]
  del data[:]