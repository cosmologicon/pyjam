from . import levels

unlocked = set(["empty"])
beaten = set()
seen = set()



def getstate():
	return unlocked, beaten, seen

def setstate(pstate):
	global unlocked, beaten, seen
	unlocked, beaten, seen = pstate

def unlockall():
	for level in levels.data:
		unlocked.add(level)
		beaten.add(level)


