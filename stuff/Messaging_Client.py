from socket import *
import os
import time

users = []

BUFFER_SIZE = 2048
IP = "192.168.1.255"
PORT = 5000

socket = socket(AF_INET, SOCK_DGRAM)
socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socket.bind((IP, PORT))
print("bound")

while True:
	msg = socket.recv(BUFFER_SIZE)
	msg = msg.decode()
	print(msg)
