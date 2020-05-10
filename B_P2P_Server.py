import socket
import os
from datetime import datetime
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
	        chunkname = content_name.replace('.png', '')+'_'+str(index)
	        chunk_addr = 'sliced_files/'+chunkname
	        with open(chunk_addr,'wb+') as chunk_file:
	            chunk_file.write(chunk)
	        index += 1
	        chunk = infile.read(int(CHUNK_SIZE))
	chunk_file.close()

ts = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # temp socket to get the wifi interface ip
ts.connect(("8.8.8.8", 80))
SERVER_IP = ts.getsockname()[0]
ts.close()
SERVER_PORT = 5001

BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER_IP, SERVER_PORT))
s.listen(2)
print("Server is listening!")

#Assumes there are no sub-directories in this directory
shared_files = os.listdir("shared_files")

#asks the user to select a file to host
for i in range(len(shared_files)):
	if shared_files[i].endswith('.png'): # discard the .png if it is in the file name
		shared_files[i] = shared_files[i].replace(".png", '');
	print(str(i) + ': ' + shared_files[i])

selection = input("Select a file number to host ")
selectedFileName = shared_files[int(selection)] + '.png'
print("Selected " + selectedFileName)

sliceFile(selectedFileName) # prepare the selected file for hosting

while True:
	try:
		conn, addr = s.accept()
		print("Connected to client with address of" + str(addr))
		reqJSON = conn.recv(BUFFER_SIZE) #the request from the client comes in as utf_8 encoded json
		print(str(reqJSON) + " was requested")
		reqJSON = json.loads(reqJSON)
		requestedChunkName = reqJSON["filename"] #load and parse the request json
		with open("sliced_files/" + requestedChunkName, 'rb') as outFile:
			totalsent = 0
			msg = bytes(outFile.read())
			while totalsent < len(msg):
				sent = conn.send(msg[totalsent:])
				totalsent += sent
				print("sent " + sent)
			with open("upload_log.txt", 'a') as up_log: # update the upload log
				now = datetime.now()
				dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
				up_log.write(dt_string + ' ' + requestedChunkName + " to " + str(addr[0]) + '\n')
		# The connection should be terminated by the client at this point

	except KeyboardInterrupt:
		conn.close()
		s.close()
		sys.exit()
	except Exception as e:
		print(e.args)
		s.close()
		sys.exit()
