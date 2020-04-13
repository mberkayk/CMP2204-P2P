from socket import *
import os
import time
import math

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

SERVER_PORT = 5001
SERVER_IP = ''
BUFFER_SIZE = 1024

socket = socket(AF_INET, SOCK_STREAM)
socket.bind((SERVER_IP, SERVER_PORT))
socket.listen(9) # at most 10 users
print("Server is listening!")

#Assumes there are no sub-directories in this directory
shared_files = os.listdir("shared_files")

for i in range(len(shared_files)):
	if shared_files[i].endswith('.png'):
		shared_files[i] = shared_files[i].replace(".png", '');
	print(str(i) + ': ' + shared_files[i])

selection = input("Select a file number to host ")
selectedFileName = shared_files[int(selection)]
print("Selected " + selectedFileName)

sliceFile(selectedFileName)

while True:
	try:
		conn, addr = socket.accept()
		print("Connected to client with address of" + str(addr))
	except KeyboardInterrupt:
		socket.close()
