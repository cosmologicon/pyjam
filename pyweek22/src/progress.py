# Overall game progress, scores, etc.
import os.path
from . import util, settings, level

try:
	import cPickle as pickle
except ImportError:
	import pickle
from . import settings

completed = set()  # levels completed
unlocked = set([1])
learned = set(["X"])
heard = set()  # dialogs heard
chosen = 1  # most recent level selected on menu

if True:
	for l in level.layout:
		unlocked.add(l)
	for learn in "X Y XX XY YY XXX XXY XYZ Z".split():
		learned.add(learn)

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
	return completed, unlocked, heard, chosen, learned

def setprogress(obj):
	global completed, unlocked, heard, chosen, learned
	completed, unlocked, heard, chosen, learned = obj

def save():
	filename = settings.progresspath
	util.mkdir(filename)
	pickle.dump(getprogress(), open(filename, "wb"))

def load():
	filename = settings.progresspath
	if not os.path.exists(filename):
		return
	setprogress(pickle.load(open(filename, "rb")))


def removesave():
	filename = settings.progresspath
	if os.path.exists(filename):
		os.remove(filename)

