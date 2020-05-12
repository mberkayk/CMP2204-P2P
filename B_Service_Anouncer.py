from socket import *
import os
import time
import json

username = input("Please enter a username: ")

#assumes there are only files in this directory and no subdirectories
sliced_files = os.listdir("sliced_files")

dictionaryPY = json.loads('{"username" : "", "files" : "" }') # constructing the advertised dictionary
dictionaryPY["username"] = username                           #not to be confused with the contentDictionary.json
dictionaryPY["files"] = sliced_files

dictionaryJSON = json.dumps(dictionaryPY)

advertisedFile = open("advertisedFile.json", 'w')
advertisedFile.write(dictionaryJSON)
advertisedFile.close()

# get the ip address of the wifi interface
s = socket(AF_INET, SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
arr = s.getsockname()[0].split('.')
s.close()
arr[3] = '255'
IP = arr[0] + '.' + arr[1] + '.' + arr[2] + '.' + arr[3] # construct the broadcast ip
# IP="25.255.255.255"
PORT = 5000

socket = socket(AF_INET, SOCK_DGRAM)
socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

lastSentTime = 0
anouncePeriod = 10
while True: # send the advertisedFile.json over the  broadcast ip every "anouncePeriod" seconds

	if time.time() - lastSentTime > anouncePeriod:
		socket.sendto(bytes(dictionaryJSON.encode("utf-8")), (IP, PORT))
		lastSentTime = time.time()
		print("sent!")

	time.sleep(10)
