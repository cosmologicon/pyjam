import pickle, os
from . import levels, settings

unlocked = set(["single"])
beaten = set()
seen = set()



def getstate():
	return unlocked, beaten, seen

def setstate(pstate):
	global unlocked, beaten, seen
	unlocked, beaten, seen = pstate

def unlockall():
	for level in levels.data:
		unlocked.add(level)
		beaten.add(level)


def save():
	pickle.dump(getstate(), open(settings.savename, "wb"))

def load():
	if os.path.exists(settings.savename):
		setstate(pickle.load(open(settings.savename, "rb")))

def reset():
	if os.path.exists(settings.savename):
		os.remove(settings.savename)


