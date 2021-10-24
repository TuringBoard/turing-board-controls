from src.Communication.communicate import SerialCommunication
from src.Communication.network import RemoteControl
import time


def main():
    s = SerialCommunication('COM9', 115200)
    print("Initiating UART thread...")
    s.start()

    remote_control = RemoteControl('127.0.0.1', 1100)
    print("Initiating Remote Control thread...")
    remote_control.start()

    # e is the exit flag
    e = False
    while not e:
        print(s.poll())

        command = remote_control.poll()
        if command:
            print(f"Input = {command}")
            s.push(command)
            s.send()

    s.join()
    remote_control.join()


if __name__ == '__main__':
    main()
