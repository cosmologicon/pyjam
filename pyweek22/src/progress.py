# Overall game progress, scores, etc.
import os.path
from . import util, settings, level, mechanics

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
nslots = 3

if settings.quickstart or settings.unlockall:
	for l in level.layout:
		unlocked.add(l)
	for learn in mechanics.towerinfo:
		learned.add(learn)
	nslots = 8

def complete(lev):
	global nslots
	from . import menuscene
	menuscene.clearmessage()
	completed.add(lev)
	for nlev in level.unlocks.get(lev, []):
		unlocked.add(nlev)
	mset = False
	for nlearn in level.learns.get(lev, []):
		if nlearn not in learned:
			learned.add(nlearn)
			if not mset:
				from . import menuscene
				menuscene.setmessage("New antibody combination unlocked!")
				mset = True
	slots = level.slots.get(lev, 0)
	if slots > nslots:
		from . import menuscene
		menuscene.setmessage("New organelle slot unlocked!")
		nslots = slots
	save()

def beatone():
	from . import menuscene
	menuscene.clearmessage()
	lev = max(x for x in unlocked if x in range(10))
	complete(lev)

def setchosen(lev):
	global chosen
	chosen = lev
	save()

def getprogress():
	from . import quest
	return completed, unlocked, heard, chosen, learned, nslots, quest.quests

def setprogress(obj):
	from . import quest
	global completed, unlocked, heard, chosen, learned, nslots
	completed, unlocked, heard, chosen, learned, nslots, quest.quests = obj

def save():
	filename = settings.progresspath
	util.mkdir(filename)
	pickle.dump(getprogress(), open(filename, "wb"))

def canload():
	return os.path.exists(settings.progresspath)

def load():
	filename = settings.progresspath
	if not os.path.exists(filename):
		return
	setprogress(pickle.load(open(filename, "rb")))


def removesave():
	filename = settings.progresspath
	if os.path.exists(filename):
		os.remove(filename)

