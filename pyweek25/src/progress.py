import os
try:
	import cPickle as pickle
except ImportError:
	import pickle
from . import settings

unlocked = set(["level1.x", "level1.y", "level1.xy", "level2.x", "level2.y"])
beaten = set()
current = None

def getstate():
	return unlocked, beaten, current
def setstate(obj):
	global unlocked, beaten, current
	unlocked, beaten, current = obj


def save():
	pickle.dump(getstate(), open(settings.savename, "wb"), 2)
def load():
	if os.path.exists(settings.savename):
		setstate(pickle.load(open(settings.savename, "rb")))
def reset():
	if os.path.exists(settings.savename):
		os.delete(settings.savename)

if settings.reset:
	reset()
load()


def select(level):
	global current
	current = level
	save()
def win():
	beaten.add(current)
	save()

