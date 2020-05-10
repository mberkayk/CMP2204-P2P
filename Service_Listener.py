from socket import *
import os
import time
import json
import sys


# get the ip address of the wifi interface
s = socket(AF_INET, SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
arr = s.getsockname()[0].split('.')
s.close()
arr[3] = '255'

IP = arr[0] + '.' + arr[1] + '.' + arr[2] + '.' + arr[3] # construct the broadcast ip
PORT = 5000

BUFFER_SIZE = 4096

# construct the socket to listen to all broadcasts
socket = socket(AF_INET, SOCK_DGRAM)
socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socket.bind((IP, PORT))
print("socket bound to the port", PORT)

contentDictionary = json.loads('{}')


onlineUsers = []

#reset the content dictionary to make sure to get rid of any data remaining from old sessions
f = open("contentDictionary.json", "w")
f.close()

#print everything that a user has
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
		incomingDictPy = json.loads(incomingDictStr) # load the incoming json broadcast

		if (incomingDictPy["username"]) not in dict(onlineUsers): # if this user is new add them the to onlineUsers
			#append a tuple with the username and the ip of the broadcasting user
			onlineUsers.append((incomingDictPy["username"], addr[0])) # addr[0] is the ip address of the broadcasting user

		cntDictModified = False # isContentDictionaryModified
		for file_chunk in incomingDictPy["files"]: # iterate through all the files in the advertised json file
			if file_chunk in contentDictionary:
				if addr[0] not in contentDictionary[file_chunk]: # if the file is already in the dictionary but the broadcasting user just started hosting it
					contentDictionary[file_chunk].append(addr[0])
					print("added " + addr[0] + " to " + file_chunk)
					cntDictModified = True
			else: # if the file is not in the dictionary
				contentDictionary[file_chunk] = []
				contentDictionary[file_chunk].append(addr[0])
				print("added " + file_chunk + " to the dictionary")
				cntDictModified = True

		if cntDictModified: # if content dictionary is modified the update the file
			cntDictFile = open("contentDictionary.json", "w")
			json.dump(contentDictionary, cntDictFile)
	except KeyboardInterrupt: # keyboard interrupt is a way to "break out of the while loop" and get inputs from user
		print() # add an empty line for readability
		i = input() # get the command
		if i == 'q': # q is for quitting the program
			cntDictFile.close()
			sys.exit()
		elif i == "online_users": # online_users command prints out all the users in the network
			print(onlineUsers)
		elif i == "cnt_dict": # prints the content dictionary
			print(json.dumps(contentDictionary, indent = 2))
		elif i.startswith("usr "): # usr keyword followed by the exact username of a user in the network, will print out all the files that user is sharing
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
