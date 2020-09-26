import math, pickle
from . import world

you = None
rmoon = world.zhat
dmoon = 40
tide = 0
moonrod = None


islands = []
effects = []
anchored = None
color0 = 0, 0, 0
cfactor = None

ntabs = 0

def tideat(pos):
	return tide * math.dot(rmoon, pos)

def iname():
	for island in islands:
		if island.distout(you.up) < 15:
			return island.name
	return None

def getisland(name):
	for island in islands:
		if island.name == name:
			return island
	return None

def act():
	global anchored
	if anchored is not None:
		anchored.unanchor()
		anchored = None
	elif moonrod is not None:
		if moonrod.anchorableto(you):
			moonrod.anchorto(you)
			anchored = moonrod


cfactor = 1
def approachcolor0(c, dt):
	global color0
	color0 = math.approach(color0, c, dt * cfactor)


def save(filename):
	from . import view, quest, sound, hud
	obj = you, rmoon, dmoon, tide, islands, effects, anchored, color0, ntabs, moonrod, cfactor, view.self, quest.quests, sound.getstate(), hud.self
	pickle.dump(obj, open(filename, "wb"))

def load(filename):
	global you, rmoon, dmoon, tide, islands, effects, anchored, color0, ntabs, moonrod, cfactor
	from . import view, quest, sound, hud
	obj = pickle.load(open(filename, "rb"))
	you, rmoon, dmoon, tide, islands, effects, anchored, color0, ntabs, moonrod, cfactor, view.self, quest.quests, soundstate, hud.self = obj
	sound.setstate(soundstate)


