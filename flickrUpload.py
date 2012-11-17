#!/usr/bin/env python

import os
import sys
import re
import flickrapi

# Check for picture file to be uploaded to Flickr
try:
	photo_path = sys.argv[1]
except IndexError:
	sys.exit("Usage: " + sys.argv[0] + " <path to photo>")

if(os.path.isfile(photo_path) == False):
	sys.exit("File not found: " + photo_path)

# Add your API Key and API Secret
api_key = ''
api_secret = ''

flickr = flickrapi.FlickrAPI(api_key, api_secret)

(token, frob) = flickr.get_token_part_one(perms='write')
if not token:
    raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

res = flickr.upload(filename=photo_path, is_public=u'1')

try:
	photo = res[0]
except IndexError:
	sys.exit("Unexpected response")

try:
	tag = photo.tag
except:
	sys.exit("Attribute 'tag' missing in result")

if tag == 'photoid':
	print 'http://www.flickr.com/photos/upload/edit/?ids=' + t.text
else:
	print 'http://www.flickr.com/upload+failed'

sys.exit(0)