from socket import *
import os
import time
import json
import sys


# get the ip address
s = socket(AF_INET, SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
arr = s.getsockname()[0].split('.')
s.close()
arr[3] = '255'

IP = arr[0] + '.' + arr[1] + '.' + arr[2] + '.' + arr[3]
PORT = 5000

BUFFER_SIZE = 4096

socket = socket(AF_INET, SOCK_DGRAM)
socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socket.bind((IP, PORT))
print("socket bound to the port", PORT)

contentDictionary = json.loads('{}')


onlineUsers = []

f = open("contentDictionary.json", "w") # reset the content dictionary
f.close()

def printUserContent(IP):
	str = ''
	str += (name + " has files:\n")
	for file_chunk in contentDictionary:
		if IP in contentDictionary[file_chunk]:
			str += (file_chunk + "\n")
	print(str)


while True:
	try:
		msg, addr = socket.recvfrom(BUFFER_SIZE)
		incomingDictStr = msg.decode("utf-8")
		incomingDictPy = json.loads(incomingDictStr)

		if (incomingDictPy["username"]) not in dict(onlineUsers):
			onlineUsers.append((incomingDictPy["username"], addr[0]))

		cntDictModified = False
		for file_chunk in incomingDictPy["files"]:
			if file_chunk in contentDictionary:
				if addr[0] not in contentDictionary[file_chunk]:
					contentDictionary[file_chunk].append(addr[0])
					print(addr[0] + "is not in" + contentDictionary[file_chunk])
					cntDictModified = True
			else:
				contentDictionary[file_chunk] = []
				contentDictionary[file_chunk].append(addr[0])
				print("added " + addr[0] + " to " + file_chunk)
				cntDictModified = True

		if cntDictModified:
			cntDictFile = open("contentDictionary.json", "w")
			json.dump(contentDictionary, cntDictFile)
	except KeyboardInterrupt:
		print() # add an emty line
		i = input()
		if i == 'q':
			cntDictFile.close()
			sys.exit()
		elif i == "online_users":
			print(onlineUsers)
		elif i == "cntDict":
			print(json.dumps(contentDictionary, indent = 2))
		elif i.startswith("usr "):
			name = i[4:]
			ip = 0
			usrExists = False
			for u in onlineUsers:
				if u[0] == name:
					ip = u[1]
					usrExists = True
					break
			if usrExists == False:
				print("This user doesn't exist!")
			else:
				printUserContent(ip)
