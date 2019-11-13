# suche dateien

import os
import time

def serarchFile(path = None, days = 1, ignoresFiles = [".DS_Store"]):
	''' retuns a filelist from "path", wich is newer then "days" from actual time '''
	fileList = os.listdir(path)
	
	timeLeft = (time.time() - days*24*60*60 )
	currentFiles = []

	for file in fileList:
		if file not in ignoresFiles:
			if os.path.getmtime(path + "/" + file) > timeLeft:
				currentFiles.append([file, os.path.getmtime(path + "/" + file) ])

	if currentFiles != []:
		return currentFiles




def searchFilesTypes(path = None, fileType = '.enc'):
	''' gibt eine liste mit Dateien zurück von dem gegebenen fileType '''

	returnList = []
	fileList = os.listdir(path)

	for f in fileList:
		if f[-4:] == fileType:
			returnList.append(f)

	return returnList



if __name__ == '__main__':
	fileList = serarchFile("testfiles")

	for item in fileList:
		print(item[0])


