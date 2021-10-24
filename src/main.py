from src.Communication.communicate import ReceiveThread
import time


def main():
    s = ReceiveThread('COM9', 115200)
    print("Starting communication thread...")
    s.start()

    # e is the exit flag
    e = False
    while not e:
        print(s.poll())
        time.sleep(1)

        s.push(b'r')
        s.send()

    s.join()


if __name__ == '__main__':
    main()
