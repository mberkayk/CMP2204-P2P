from socket import *
import os

IP = "192.168.1.255"

PORT = 5000

socket = socket(AF_INET, SOCK_DGRAM)
socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

lastSentTime = 0
anouncePeriod = 10
while True:
	msg = input('>>')
	msg = msg.encode()
	socket.sendto(msg, (IP, PORT))
