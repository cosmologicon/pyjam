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
	
	"C0": (7, 3),
	"C1": (7, 1),
	
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

	("tutorial4", "C0"),
	("C0", "C1"),
	("A1", "A2"),

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

def unlockall():
	global unlocked
	unlocked = set(stages)

