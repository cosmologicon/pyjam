stages = {
	"backyard": (2, 3),
	"stage 2": (3, 2),
	"lair": (4, 2),
	"boss": (4, 3),
}
joins = [
	("backyard", "stage 2"),
	("stage 2", "lair"),
	("stage 2", "boss"),
	("lair", "boss"),
	("backyard", "boss"),
]
at = "backyard"
unlocked = set(["backyard"])
beaten = set()

def beat(level):
	global unlocked
	beaten.add(level)
	for pair in joins:
		if level in pair:
			unlocked |= set(pair)

def unlockall():
	global unlocked
	unlocked = set(stages)

