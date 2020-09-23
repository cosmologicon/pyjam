import math
from . import world

you = None
rmoon = world.zhat
tide = 0

islands = []


def tideat(pos):
	return tide * math.dot(rmoon, pos)
	
