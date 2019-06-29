from __future__ import print_function

# Python 2 and 3: easiest option
# https://python-future.org/compatible_idioms.html
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlencode
from urllib.request import urlopen

import json, os.path
from . import settings

if not os.path.exists(settings.gallerydir):
	os.mkdir(settings.gallerydir)

def upload(makername, designname, design):
	if settings.offline:
		return
	data = {
		"makername": makername,
		"designname": designname,
		"design": design.getspec(),
	}
	url = settings.serverurl + "cgi-bin/share.py"
	data = urlencode([("data", json.dumps(data))]).encode()
	response = urlopen(url, data)
	if settings.DEBUG:
		print("RESPONSE", response.read())
	return response.read()

def pullgallery():
	if settings.offline:
		return
	data = {
		"excludes": list(os.listdir(settings.gallerydir)),
	}
	url = settings.serverurl + "cgi-bin/pullgallery.py"
	data = urlencode([("data", json.dumps(data))])
	response = ""
	try:
		response = urlopen(url + "?" + data).read().decode('utf-8')
		if settings.DEBUG:
			print("RESPONSE", response[:200])
		rdata = json.loads(response)
		for filename, contents in rdata:
			filename = os.path.basename(filename)
			if len(contents) > 100000:
				continue
			contents = json.dumps(json.loads(contents))
			open(os.path.join(settings.gallerydir, filename), "w").write(contents)
	except Exception as e:
		print()
		print("Error retrieving gallery from server. Switching to offline mode.")
		print(e)
		if response:
			print("Response: ")
			print(response[:2000])
		print()
		print("See README.txt for starting in offline mode if the problem persists.")
		settings.offline = True


