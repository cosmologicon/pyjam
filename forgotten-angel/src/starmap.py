import pygame
try:
	import cPickle as pickle
except ImportError:
	import pickle

def init():
	global ps, oortdata, scale, rx, ry, oortmap
	obj = pickle.load(open("data/starmap.pkl", "rb"))
	ps, oortdata, scale, rx, ry = obj

def getoort(p):
	x, y = p
	key = int(round((x + rx) * scale)), int(round((y + ry) * scale))
	if key in oortdata:
		return oortdata[key]
	else:
		return 1

