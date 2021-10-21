from src.Communication.communicate import SerialCommunication
import time


def main():
    s = SerialCommunication('COM9', 115200)
    print("Starting communication thread...")
    s.start()

    # e is the exit flag
    e = False
    while not e:
        print(s.poll())
        time.sleep(1)

    s.join()


if __name__ == '__main__':
    main()
