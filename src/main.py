from src.Communication.communicate import SerialCommunication
from src.Communication.network import RemoteControl
import time


def main():
    s = SerialCommunication('COM9', 115200)
    print("Starting communication thread...")
    s.start()

    remote_control = RemoteControl()
    print("Starting remote control thread...")
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

        time.sleep(1)

    s.join()
    remote_control.join()


if __name__ == '__main__':
    main()
