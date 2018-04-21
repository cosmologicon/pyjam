import os
try:
	import cPickle as pickle
except ImportError:
	import pickle
from . import settings

unlocked = set(["level1.act1", "level3.act1", "level5.act1"])
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
		os.remove(settings.savename)

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

