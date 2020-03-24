from socket import *

serverPort = 5005;
serverIP = '0.0.0.0'
bufferSize = 1024

socket = socket(AF_INET, SOCK_STREAM)

socket.connect((serverIP, serverPort))

while True :
	msg = input("Press enter to send stuff")

	if msg == "quit()" :
		socket.close()
		break
	else:
		socket.send(msg.encode('ascii'))
