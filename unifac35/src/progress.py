import pickle, os.path
from . import settings

stages = {
	(0, 0): "alfa",
	(2, 2): "bravo",
	(-2, 2): "1",
}

unlocks = {
	"alfa": "1",
}

unlocked = set(["alfa", "bravo"])
completed = set()

def save():
	obj = unlocked, completed
	pickle.dump(obj, open(settings.savefile, "wb"))

def load():
	global unlocked, completed
	if os.path.exists(settings.savefile):
		obj = pickle.load(open(settings.savefile, "b"))
		unlocked, completed = obj

def complete(stagename):
	completed.add(stagename)
	if stagename in unlocks:
		for unlock in unlocks[stagename]:
			unlocked.add(unlock)
	save()


