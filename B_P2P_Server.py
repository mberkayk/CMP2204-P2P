from socket import *
import os
import time
import math
import sys
import json

def sliceFile(content_name):
	fileURL = 'shared_files/'+content_name
	c = os.path.getsize(fileURL)
	CHUNK_SIZE = math.ceil(math.ceil(c)/5)

	index = 1
	with open(fileURL, 'rb') as infile:
	    chunk = infile.read(int(CHUNK_SIZE))
	    while chunk:
	        chunkname = content_name+'_'+str(index)
	        chunk_addr = 'sliced_files/'+chunkname
	        with open(chunk_addr,'wb+') as chunk_file:
	            chunk_file.write(chunk)
	        index += 1
	        chunk = infile.read(int(CHUNK_SIZE))
	chunk_file.close()

s = socket(AF_INET, SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
SERVER_IP = s.getsockname()[0]
s.close()
SERVER_PORT = 5001

BUFFER_SIZE = 4096

socket = socket(AF_INET, SOCK_STREAM)
socket.bind((SERVER_IP, SERVER_PORT))
socket.listen(1)
print("Server is listening!")

#Assumes there are no sub-directories in this directory
shared_files = os.listdir("shared_files")

for i in range(len(shared_files)):
	if shared_files[i].endswith('.png'):
		shared_files[i] = shared_files[i].replace(".png", '');
	print(str(i) + ': ' + shared_files[i])

selection = input("Select a file number to host ")
selectedFileName = shared_files[int(selection)] + '.png'
print("Selected " + selectedFileName)

sliceFile(selectedFileName)

while True:
	try:
		conn, addr = socket.accept()
		print("Connected to client with address of" + str(addr))
		reqJSON = conn.recv(BUFFER_SIZE) #comes in as utf_8 encoded json
		print(reqJSON)
		reqJSON = json.loads(reqJSON)
		requestedChunkName = reqJSON["filename"]
		with open("sliced_files/" + requestedChunkName, 'rb') as outFile:
			conn.send(bytes(outFile.read()))
		conn.close()

	except KeyboardInterrupt:
		conn.close()
		socket.close()
	except:
		socket.close()
