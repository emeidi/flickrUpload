#!/usr/bin/env python

import os
import sys
import re
import flickrapi

# Variables
api_creds_file = 'apiCreds.txt'

# Check for picture file to be uploaded to Flickr
try:
	photo_path = sys.argv[1]
except IndexError:
	sys.exit("Usage: " + sys.argv[0] + " <path to photo>")

if(os.path.isfile(photo_path) == False):
	sys.exit("File not found: " + photo_path)

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
    raw_input("Press ENTER after you have authorized this program")
flickr.get_token_part_two((token, frob))

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