stages = {
	"tutorial1": (4, 3),
	"tutorial2": (5, 2),
	"tutorial3": (6, 3),
	"tutorial4": (7, 2),
	"nexus": (4, 5.5),
	"finale": (4, 10.5),
}
joins = [
#	("nexus", "finale"),
	("tutorial1", "nexus"),

	("tutorial1", "tutorial2"),
	("tutorial2", "tutorial3"),
	("tutorial3", "tutorial4"),
]
at = "tutorial1"
unlocked = set(["tutorial1"])
beaten = set()
dseen = set()

def beat(level):
	global unlocked
	beaten.add(level)
	for pair in joins:
		if level in pair:
			unlocked |= set(pair)

def unlockall():
	global unlocked
	unlocked = set(stages)

