import socket
import json
from datetime import datetime

def combineSlices(content_name):
	chunknames = [content_name+'_1', content_name+'_2', content_name+'_3', content_name+'_4', content_name+'_5']

	with open("shared_files/" + content_name+'.png', 'wb') as outfile:
	    for chunk in chunknames:
	        with open("sliced_files/" + chunk, 'rb') as infile:
	            outfile.write(infile.read())

PORT = 5001
BUFFER_SIZE = 8192

contentDictionaryFile = open("contentDictionary.json", 'rt')
contentDictionary = json.load(contentDictionaryFile)

while True:

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
	allChunksDownloaded = True
	for i in range(1, 6): #iterate through chunks
		chunkToDownload = availableFiles[selectedFileIndex] + "_" + str(i) # construct the chunk name
		#construct the request json file
		requestPy["filename"] = chunkToDownload
		requestJSON = json.dumps(requestPy)

		chunkIsDownloaded = False
		for ip in contentDictionary[chunkToDownload]: # iterate through users who are serving the chunk
			print("asking " + ip + ' for ' + chunkToDownload)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(10)
			try:
				#try to connect to the user and download chunk
				s.connect((ip, PORT))
				s.send(bytes(requestJSON, "utf-8"))
				print(requestJSON + " was requested")
				downloadedChunk = s.recv(BUFFER_SIZE)
				msg = downloadedChunk
				while len(msg) == BUFFER_SIZE:
					print("recieved message")
					msg = s.recv(BUFFER_SIZE)
					downloadedChunk += msg
				chunkIsDownloaded = True
			except Exception as e:
				s.close()
				print("Couldn't download " + chunkToDownload + " from " + ip)
				print(e)
				continue

		if chunkIsDownloaded:
			#update the download log
			with open("download_log.txt", 'a') as up_log:
				now = datetime.now()
				dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
				up_log.write(dt_string + ' ' + chunkToDownload + " from " + str(ip) + '\n')
			#save the downloaded chunk to /sliced_files
			with open("sliced_files/" + chunkToDownload, 'wb') as downloadedFile:
				downloadedFile.write(downloadedChunk)
			downloadedFile.close()
			s.close() # close the connection to the user who served the chunk
			print("Chunk downloaded successfully")
		else:
			allChunksDownloaded = False
			print("Chunk wasn't downloaded")
			break
	if allChunksDownloaded:
		print("Download finished succesfully!")
		combineSlices(availableFiles[selectedFileIndex])
	else:
		print("Download Failed!")
