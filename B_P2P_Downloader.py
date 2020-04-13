from socket import *
import json

contentDictionaryFile = open("contentDictionary.json", 'rt')
contentDictionary = json.load(contentDictionaryFile)

#parse contentDictionary for the available files to download
availableFiles = []

for fileChunk in contentDictionary:
	fileName = str(fileChunk)[:len(fileChunk)-2] # get rid of the number
	if fileName not in availableFiles:
		availableFiles.append(fileName)

#Select a file to request
print("Enter the index of the file you want to download")
for i in range(len(availableFiles)):
	print(str(i) +": " + availableFiles[i])

selectedFileIndex = int(input())

#request the file
requestPy = {
	"filename": ""
}
PORT = 5001
BUFFER_SIZE = 1024
socket = socket(AF_INET, SOCK_STREAM)
for i in range(1, 6):
	chunkToDownload = availableFiles[selectedFileIndex] + "_" + str(i)
	requestPy["filename"] = chunkToDownload
	requestJSON = json.dumps(requestPy)

	for ip in contentDictionary[chunkToDownload]:
		print(ip + ' for ' + chunkToDownload)
		socket.connect((ip, PORT))
		socket.send(bytes(requestJSON))
