#!/usr/bin/env python

import os
import sys
import re
import flickrapi

# Variables
api_creds_file = 'apiCreds.txt'

# Functions
def debugMsg(msg,type='Info'):
	out = ""
	out += type.upper() + ":" + "\n"
	out += "    " + msg + "\n" + "\n"

	print out
	#debugFileStream.write(out)

def checkArgs():
	numArgs = len(sys.argv)
	if (numArgs < 2):
		return False
	return True

def offerFiles():
	workingDir = os.getcwd()
	
	debugMsg('Looking for files in ' + workingDir)

	counter = 0
	matchingFiles = {}
	for file in os.listdir(workingDir):
		#if fnmatch.fnmatch(file, defaultInputFilePattern):
		if re.search('^[^\.].*\.(jpg|jpeg|gif|bmp|png)$',file,re.IGNORECASE) != None:
			counter += 1
			matchingFiles[counter] = file
			print(str(counter) + ") " + file)

	if counter < 1:
		debugMsg('No ' + defaultInputFilePattern + ' files found in current directory. Please provide a path to the input file.','Info')
		filenameInput = raw_input("Input file (." + defaultInputFilePattern + "): ")
	else:
		print("")
		keyInput = int(raw_input("Input file number: "))

		if keyInput in matchingFiles:
			filenameInput = matchingFiles[keyInput]
		else:
			debugMsg('Option ' + str(keyInput) + ') does not exist ','Error')
			debugMsg('Please enter the filename by yourself','Info')
			filenameInput = raw_input("Input file (" + defaultInputFilePattern + "): ")
	
	#filenameOutput = raw_input("Output file (.xlsx): ")
	#print("")
	
	return filenameInput

# Store API Key and API Secret in the file api_creds_path in the script directory
# Separate the API Key and the API Secret with a ":" (colon)
api_creds_path = os.path.dirname(__file__) + '/' + api_creds_file
if(os.path.isfile(api_creds_path) == False):
	sys.exit("File not found: " + api_creds_path)

(api_key, api_secret) = open(api_creds_path).read().strip().split(':')
#print "Using API Key '" + api_key + "' and API Secret '" + api_secret + "'"

flickr = flickrapi.FlickrAPI(api_key, api_secret)

(token, frob) = flickr.get_token_part_one(perms='write')
if not token:
    raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

# Check file
numArgs = len(sys.argv)
if(numArgs < 1):
	debugMsg("Usage:" + sys.argv[0] + " <path to photo>",'Error')
	sys.exit(1)


if checkArgs():
	photo_path = sys.argv[1]
else:
	photo_path = offerFiles()

if(os.path.isfile(photo_path) == False):
	debugMsg("File not found: " + photo_path)
	sys.exit(1)

res = flickr.upload(filename=photo_path, is_public=u'1')

try:
	photo = res[0]
except IndexError:
	sys.exit("Unexpected response")

try:
	tag = photo.tag
except AttributeError:
	sys.exit("Attribute 'tag' missing in result")

if tag != 'photoid':
	sys.exit("Cannot retrieve photoid from response")

print 'http://www.flickr.com/photos/upload/edit/?ids=' + photo.text
sys.exit(0)