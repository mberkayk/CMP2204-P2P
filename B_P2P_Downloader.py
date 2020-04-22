import socket
import json

def combineSlices(content_name):
	chunknames = [content_name+'_1', content_name+'_2', content_name+'_3', content_name+'_4', content_name+'_5']

	with open("shared_files/" + content_name+'.png', 'wb') as outfile:
	    for chunk in chunknames:
	        with open("sliced_files/" + chunk, 'rb') as infile:
	            outfile.write(infile.read())

contentDictionaryFile = open("contentDictionary.json", 'rt')
while True:
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
	BUFFER_SIZE = 4096
	allChunksDownloaded = True
	for i in range(1, 6):
		chunkToDownload = availableFiles[selectedFileIndex] + "_" + str(i)
		requestPy["filename"] = chunkToDownload
		requestJSON = json.dumps(requestPy)

		chunkDownloaded = False
		for ip in contentDictionary[chunkToDownload]:
			print("asking " + ip + ' for ' + chunkToDownload)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				s.connect((ip, PORT))
				s.send(bytes(requestJSON, "utf-8"))
				downloadedChunk = s.recv(BUFFER_SIZE)
			except Exception as e:
				s.close()
				print("Couldn't download " + chunkToDownload + " from " + ip)
				print(e)
				continue
			with open("sliced_files/" + chunkToDownload, 'wb') as downloadedFile:
				downloadedFile.write(downloadedChunk)
			downloadedFile.close()
			s.close()
			chunkDownloaded = True
			break
		if chunkDownloaded:
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
