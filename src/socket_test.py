# This program will be used to test the P2P connection between the remote control and long board

import socket


ip = '127.0.0.1'
remote_control_port = 1100

# IPv4, TCP Stream Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, remote_control_port))
s.listen()
print("Waiting to receive a connection...")
conn, address = s.accept()
print(f'Received connection from {address}')

while True:
    print('Turing Board> ', end="")
    user_input = input()
    conn.sendall(bytes(user_input, 'ascii'))
