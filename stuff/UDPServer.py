from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	print("received!")
	modifiedMessage = message.decode('utf-8').upper()
	serverSocket.sendto(modifiedMessage.encode('utf-8'), clientAddress)
	print("and sent")
