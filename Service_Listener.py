from socket import *
import os
import time

users = []

BUFFER_SIZE = 2048
IP = "192.168.1.255"
PORT = 5000

socket = socket(AF_INET, SOCK_DGRAM)
socket.bind((IP, PORT))
print("bind")

while True:
	msg = socket.recv(BUFFER_SIZE)
	msg = msg.decode()
	flag = False
	for usr in users:
		if usr == msg:
			flag = True
			break

	if flag == True:
		print("Recieved user is already in the array")
	else:
		users.append(msg)
		print("Added new user to the array " + msg)
