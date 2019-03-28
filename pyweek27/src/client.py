from __future__ import print_function

import urllib.request, urllib.parse, json, os.path
from . import settings

if not os.path.exists(settings.gallerydir):
	os.mkdir(settings.gallerydir)

def upload(makername, designname, design):
	data = {
		"makername": makername,
		"designname": designname,
		"design": design.getspec(),
	}
	url = settings.serverurl + "cgi-bin/share.py"
	data = urllib.parse.urlencode([("data", json.dumps(data))]).encode()
	response = urllib.request.urlopen(url, data)
	return response.read()

def pullgallery():
	data = {
		"excludes": list(os.listdir(settings.gallerydir)),
	}
	url = settings.serverurl + "cgi-bin/pullgallery.py"
	data = urllib.parse.urlencode([("data", json.dumps(data))])
	response = urllib.request.urlopen(url + "?" + data).read()
	if settings.DEBUG:
		print("RESPONSE", response[:200])
	try:
		rdata = json.loads(response)
		for filename, contents in rdata:
			filename = os.path.basename(filename)
			if len(contents) > 100000:
				continue
			contents = json.dumps(json.loads(contents))
			open(os.path.join(settings.gallerydir, filename), "w").write(contents)
	except Exception as e:
		print("Error retrieving gallery from server.")
		print(e)
		print("Response: ")
		print(response)


