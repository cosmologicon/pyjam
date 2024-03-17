import math
from functools import cache

s = math.sqrt(3) / 2

# G: game coordinates
# H: hex coordinates

adjsH = [[0, 1], [1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1]]

def GconvertH(pH):
	xH, yH = pH
	return [xH, (yH + 0.5 * xH) * s]

def HadjsH(pH):
	xH, yH = pH
	return [(xH + dxH, yH + dyH) for dxH, dyH in adjsH]

def HconvertG(pG):
	xG, yG = pG
	return [xG, yG / s - 0.5 * xG]

def Gdist(pG0, pG1):
	xG0, yG0 = pG0
	xG1, yG1 = pG1
	return math.hypot(xG1 - xG0, yG1 - yG0)

def HnearestHG(pH, pG):
	xH, yH = pH
	xH, yH = int(math.floor(xH)), int(math.floor(yH))
	pHs = [(xH + dxH, yH + dyH) for dxH in (0, 1) for dyH in (0, 1)]
	return min(pHs, key = lambda pHnear: Gdist(pG, GconvertH(pHnear)))

def HnearestG(pG):
	return HnearestHG(HconvertG(pG), pG)

@cache
def Hrect(R):
	ret = set()
	for xH in range(-R, R + 1):
		for yH in range(-R, R + 1):
			if abs(xH + yH) <= R:
				ret.add((xH, yH))
	return frozenset(ret)


