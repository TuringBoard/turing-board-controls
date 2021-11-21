# This program will be used to test the P2P connection between the remote control and long board
'''
import socket


ip = '127.0.0.1'
remote_control_port = 1100

# IPv4, TCP Stream Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, remote_control_port))

while True:
    print('Turing Board> ', end="")
    user_input = input()
    s.sendall(bytes(user_input, 'ascii'))
'''

import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDNS6tW71-jOsGKOGrh6V5dQWTfZSS6tCI",
    "databaseURL": "https://turing-board-default-rtdb.firebaseio.com/",
    "authDomain": "turing-board.firebaseapp.com",
    "projectId": "turing-board",
    "storageBucket": "turing-board.appspot.com",
    "messagingSenderId": "1008426809841",
    "appId": "1:1008426809841:web:0e490af3b6046f64aeec50"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


def stream_handler(message):
    print(message["data"])


db.child("users/gXcA4yBykAS05reLm4guWoIn8D12").stream(stream_handler)
