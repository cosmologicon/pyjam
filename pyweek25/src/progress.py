import os
try:
	import cPickle as pickle
except ImportError:
	import pickle
from . import settings, dialog

unlocked = set([
	"act0.level1", "act0.level2",
	"act1.level1", "act1.level3", "act1.level5",
	"act3.level1", "act3.level3", "act3.level5",
])
beaten = set()
current = None
seen = set()

def getstate():
	return unlocked, beaten, current, seen
def setstate(obj):
	global unlocked, beaten, current, seen
	unlocked, beaten, current, seen = obj


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
def shouldtalk():
	return current in dialog.texts and current not in seen
