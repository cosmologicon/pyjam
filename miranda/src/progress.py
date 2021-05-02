import pickle, os.path, os
from . import settings

stages = {
	"tutorial1": (3, 6),
	"tutorial2": (4, 5),
	"tutorial3": (5, 4),
	"tutorial4": (6, 4),

	"A0": (4, 3),
	"A1": (3, 2),
	"A2": (1.5, 2),
	
#	"B0": (5, 2),
#	"B1": (6, 2),
	
	"C0": (5, 2),
	"C1": (7, 2),
	"C2": (8, 3),
	
	"D0": (7, 5),
	"D1": (7, 7),
	"D2": (8, 6),

	"nexus": (4, 7),
	"finale0": (4, 13),
	"finale1": (2, 13),
}
joins = [
	("tutorial1", "nexus"),
	("nexus", "finale0"),
	("finale1", "finale0"),

	("tutorial2", "A0"),
	("A0", "A1"),
	("A1", "A2"),

#	("tutorial3", "B0"),
#	("B0", "B1"),

	("tutorial3", "C0"),
	("C0", "C1"),
	("C1", "C2"),

	("tutorial4", "D0"),
	("D0", "D1"),
	("D1", "D2"),

	("tutorial1", "tutorial2"),
	("tutorial2", "tutorial3"),
	("tutorial3", "tutorial4"),
]
reqs = {
	"A0": ["tutorial4"],
	"C0": ["tutorial4"],
	"D0": ["tutorial4"],
	"nexus": ["tutorial4"],
}

# Progress state
at = "tutorial1"
unlocked = set(["tutorial1"])
beaten = set()
dseen = set()

def beat(level):
	global unlocked
	beaten.add(level)
	for pair in joins:
		if set(pair) & beaten:
			for tocheck in pair:
				if all(req in beaten for req in reqs.get(tocheck, [])):
					unlocked.add(tocheck)
	save()

def unlockall():
	global unlocked
	unlocked = set(stages)


def save():
	obj = at, unlocked, beaten, dseen
	pickle.dump(obj, open(settings.savename, "wb"))
	
def load():
	global at, unlocked, beaten, dseen
	if os.path.exists(settings.savename):
		obj = pickle.load(open(settings.savename, "rb"))
		at, unlocked, beaten, dseen = obj

def reset():
	if os.path.exists(settings.savename):
		os.remove(settings.savename)

if settings.reset:
	reset()
else:
	load()

