# Overall game progress, scores, etc.
import os.path
from . import util, settings, level

try:
	import cPickle as pickle
except ImportError:
	import pickle
from . import settings

completed = set()  # levels completed
unlocked = set([0, 1])
heard = set()  # dialogs heard
chosen = 0  # most recent level selected on menu

if True:
	unlocked.add("qwin")
	unlocked.add("endless")

def complete(lev):
	completed.add(lev)
	for nlev in level.unlocks.get(lev, []):
		unlocked.add(nlev)
	save()

def setchosen(lev):
	global chosen
	chosen = lev
	save()

def getprogress():
	return completed, unlocked, heard, chosen

def setprogress(obj):
	global completed, unlocked, heard, chosen
	completed, unlocked, heard, chosen = obj

def save():
	filename = settings.progresspath
	util.mkdir(filename)
	pickle.dump(getprogress(), open(filename, "wb"))

def load():
	filename = settings.progresspath
	if not os.path.exists(filename):
		return
	setprogress(pickle.load(open(filename, "rb")))

