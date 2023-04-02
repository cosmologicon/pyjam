import pickle, os.path
from . import settings

stages = {
#	(0, 0): "alfa",
#	(-2, 2): "1",
#	(2, -2): "playground",
	
	(-3, 4): "tutorial0",
	(-1, 4): "tutorial1",
	(1, 3): "tutorial2",
	(3, 1): "tutorial3",

	(-1, 2): "charlie",
	(1, 1): "bravo",

	(-2, 1): "bishop0",
	(-1, -1): "bishop1",
	(2, -1): "rook1",
	(1, -2): "rook0",
	
	(0, -3): "delta",
	(0, 0): "finale",
	
	(4, -4): "quit",
}


unlocks = {
	"tutorial1": ["tutorial0"],
	"tutorial2": ["tutorial1"],
	"tutorial3": ["tutorial2"],
	"charlie": ["tutorial3"],
	"bravo": ["tutorial3"],
	"bishop0": ["charlie"],
	"rook1": ["bravo"],
	"bishop1": ["bishop0"],
	"rook0": ["rook1"],
	"delta": ["bishop1", "rook0"],
	"finale": ["delta"],
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
	for stage, prereqs in unlocks.items():
		if all(s in completed for s in prereqs):
			unlocked.add(stage)
	save()

def unlockall():
	global unlocked
	unlocked |= set(stages.values())

if not settings.reset:
	load()
if settings.unlockall:
	unlockall()


