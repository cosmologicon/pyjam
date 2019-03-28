#!/usr/bin/env python

import cgi, json, sys, tempfile, os

sys.stderr = sys.stdout
data = cgi.FieldStorage().getfirst("data")
print("Content-type: text/plain\n")
limit = 40000
if len(data) > limit:
	print("Upload not accepted - exceeds %s bytes" % limit)
	exit()
data = json.dumps(json.loads(data))
ddir = "uploads"
if len(os.listdir(ddir)) > 2000:
	print("Upload not accepted - gallery is full.")
	exit()
fd, _ = tempfile.mkstemp(suffix = ".json", prefix = "", dir = ddir)
os.write(fd, data)
os.close(fd)
print("Upload accepted")

