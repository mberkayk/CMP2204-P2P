from socket import *
import os
import time

# username = input("Please enter a username")
# usrNameFileAddr = "username.txt"
# usrnameFile = open(usrNameFileAddr, 'w')
# usrnameFile.write(username)
# usrNameFileSize = os.path.getsize(usrNameFileAddr)

# IP = "192.168.1.255"
IP = "255.255.255.255"

PORT = 5000

socket = socket(AF_INET, SOCK_DGRAM)
socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

lastSentTime = 0
anouncePeriod = 10
while True:
	# if time.time() - lastSentTime > anouncePeriod:
	# 	socket.sendto(username.encode(), (IP, PORT))
	# 	lastSentTime = time.time()
	# 	print("sent!")
	msg = input('>>')
	msg = msg.encode()
	socket.sendto(msg, (IP, PORT))
