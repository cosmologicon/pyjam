# Frame-by-frame game state. Can be reset without loss of progress.

try:
	import cPickle as pickle
except ImportError:
	import pickle
import os, os.path
from . import util, progress, settings

drawables = []
colliders = []
mouseables = []
thinkers = []
buildables = []
shootables = []

groups = drawables, colliders, mouseables, thinkers, buildables, shootables

def resetgroups():
	for group in groups:
		del group[:]

def setgroups(obj):
	for x, y in zip(obj, groups):
		y[:] = x

def updatealive():
	for group in groups:
		group[:] = [m for m in group if m.alive]

def removeobj(obj):
	temp = obj.alive
	obj.alive = False
	updatealive()
	obj.alive = temp

def save():
	obj = progress.getprogress(), groups, atp, amoeba, health
	filename = settings.statepath
	util.mkdir(filename)
	pickle.dump(obj, open(filename, "wb"))

def canload():
	filename = settings.statepath
	return os.path.exists(filename)

def load():
	global atp, amoeba, health
	filename = settings.statepath
	obj = pickle.load(open(filename, "rb"))
	pstate, g, atp, amoeba, health = obj
	progress.setprogress(pstate)
	setgroups(g)

def removesave():
	filename = settings.statepath
	if os.path.exists(filename):
		os.remove(filename)


