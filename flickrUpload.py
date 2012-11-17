#!/usr/bin/env python

import os
import sys
import re
import flickrapi

# Add your API Key and API Secret
api_key = ''
api_secret = ''

flickr = flickrapi.FlickrAPI(api_key, api_secret)

(token, frob) = flickr.get_token_part_one(perms='write')
if not token:
    raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

numArgs = len(sys.argv)
if(numArgs < 1):
	sys.exit("Usage:" + sys.argv[0] + " <path to photo>")

photo_path = sys.argv[1]

if(os.path.isfile(photo_path) == False):
	sys.exit("File not found: " + photo_path)

res = flickr.upload(filename=photo_path, is_public=u'1')

t = res[0]
if t.tag == 'photoid':
	print 'http://www.flickr.com/photos/upload/edit/?ids=' + t.text
else:
	print 'http://www.flickr.com/upload+failed'

sys.exit(0)