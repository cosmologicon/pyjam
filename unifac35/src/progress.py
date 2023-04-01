import pickle, os.path
from . import settings

stages = {
#	(0, 0): "alfa",
#	(2, 2): "bravo",
#	(-2, 2): "1",
#	(2, -2): "playground",
	
	(0, 3): "tutorial0",
	(1, 2): "tutorial1",
	(2, 2): "tutorial2",
	(3, 1): "tutorial3",
	
	(0, -3): "bishop0",
	(4, -4): "rook0",
	
	(0, 0): "finale",
}

unlocks = {
	"alfa": "1",
#	"tutorial0": "tutorial1",
}

unlocked = set(["tutorial0"])
completed = set()

def save():
	obj = unlocked, completed
	pickle.dump(obj, open(settings.savefile, "wb"))

def load():
	global unlocked, completed
	if os.path.exists(settings.savefile):
		obj = pickle.load(open(settings.savefile, "rb"))
		unlocked, completed = obj

def complete(stagename):
	completed.add(stagename)
	if stagename in unlocks:
		for unlock in unlocks[stagename]:
			unlocked.add(unlock)
	save()

def unlockall():
	global unlocked
	unlocked |= set(stages.values())

if not settings.reset:
	load()
if settings.unlockall:
	unlockall()


