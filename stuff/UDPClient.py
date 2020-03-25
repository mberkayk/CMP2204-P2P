from socket import *
serverPort = 12000
serverName = 'hostname'
clientSocket = socket(AF_INET, SOCK_DGRAM)
messageStr = input("Input lowercase sentence: ")
clientSocket.sendto(messageStr.encode('utf-8'), ('0.0.0.0', serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print (modifiedMessage.decode('utf-8'))
