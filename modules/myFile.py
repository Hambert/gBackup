# files

import json
import os

def write_to_file(data, fileName = "test.json"):

	with open(fileName, "w") as write_file:
	    json.dump(data, write_file)

def read_from_file(fileName = "test.json"):
	with open( fileName , "r") as read_file:
		data = json.load(read_file)

	return data


if __name__ == '__main__':
	write_to_file(['physics', 'chemistry', 1997, 2000])

	data = read_from_file("filelist.json")

	for file in data:
		print(file["name"])