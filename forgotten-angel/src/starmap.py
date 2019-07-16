import cPickle, pygame

def init():
	global ps, oortdata, scale, rx, ry, oortmap
	obj = cPickle.load(open("data/starmap.pkl", "rb"))
	ps, oortdata, scale, rx, ry = obj

def getoort((x, y)):
	key = int(round((x + rx) * scale)), int(round((y + ry) * scale))
	if key in oortdata:
		return oortdata[key]
	else:
		return 1

