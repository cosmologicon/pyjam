import math
from . import world

you = None
rmoon = world.zhat
tide = 0

islands = []
effects = []
anchored = None

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
		print(anchored)
		anchored.unanchor()
		anchored = None
	elif moonrod is not None:
		if moonrod.anchorableto(you):
			moonrod.anchorto(you)
			anchored = moonrod
		

