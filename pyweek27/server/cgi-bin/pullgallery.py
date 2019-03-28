#!/usr/bin/env python

import cgi, json, sys, os, random, glob

sys.stderr = sys.stdout
data = cgi.FieldStorage().getfirst("data")
print("Content-type: text/plain\n")
limit = 40000
if len(data) > limit:
	print("Request rejected - exceeds %s bytes" % limit)
	exit()
data = json.loads(data)
excludes = set(data["excludes"])
files = set(os.path.basename(f) for f in glob.glob("gallery/*.json"))
files = list(files - excludes)
random.shuffle(files)
files = files[:100]
rdata = [(f.split("/")[1], open(f).read()) for f in files]
print(json.dumps(rdata))


