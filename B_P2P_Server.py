from socket import *

serverPort = 5005;
serverIP = '0.0.0.0'
bufferSize = 1024

socket = socket(AF_INET, SOCK_STREAM)
socket.bind((serverIP, serverPort))
socket.listen(9)

print("Server is listening!")

conn, addr = socket.accept()
print("Connected to client with address of" + str(addr))

conn, addr = socket.accept()
print("Connected to client with address of" + str(addr))

receivedMsg = conn.recv(bufferSize)


socket.close()
