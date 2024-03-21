import math
from functools import cache

s = math.sqrt(3) / 2

# G: game coordinates
# H: hex coordinates

adjsH = [[0, 1], [1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1]]
outlinedH = [[1/3, 1/3], [2/3, -1/3], [1/3, -2/3],
	[-1/3, -1/3], [-2/3, 1/3], [-1/3, 2/3]]
adjsetH = set((dx, dy) for dx, dy in adjsH)
adjdirH = {(dx, dy): j for j, (dx, dy) in enumerate(adjsH)}

# Distance from the center in the hex metric.
def normH(pH):
	xH, yH = pH
	return max(abs(xH), abs(yH), abs(xH + yH))
	

def HadjsH(pH):
	xH, yH = pH
	return [(xH + dxH, yH + dyH) for dxH, dyH in adjsH]

def isadjH(pH0, pH1):
	xH0, yH0 = pH0
	xH1, yH1 = pH1
	return (xH1 - xH0, yH1 - yH0) in adjsetH

def dirH(pH0, pH1):
	xH0, yH0 = pH0
	xH1, yH1 = pH1
	return adjdirH.get((xH1 - xH0, yH1 - yH0))

# pH1 is the midpoint of the segment [pH0, pH2]
def isrowH(pH0, pH1, pH2):
	xH0, yH0 = pH0
	xH1, yH1 = pH1
	xH2, yH2 = pH2
	return xH1 - xH0 == xH2 - xH1 and yH1 - yH0 == yH2 - yH1

# Returns pH2 such that (pH0, pH1, pH2) are a row.
def HpastH(pH0, pH1):
	xH0, yH0 = pH0
	xH1, yH1 = pH1
	return 2 * xH1 - xH0, 2 * yH1 - yH0

def issharpH(pH0, pH1, pH2):
	xH0, yH0 = pH0
	xH1, yH1 = pH1
	xH2, yH2 = pH2
	dG0 = GconvertH((xH1 - xH0, yH1 - yH0))
	dG1 = GconvertH((xH2 - xH1, yH2 - yH1))
	return math.dot(dG0, dG1) < 0

def GconvertH(pH):
	xH, yH = pH
	return xH, (yH + 0.5 * xH) / s

def HconvertG(pG):
	xG, yG = pG
	return xG, yG * s - 0.5 * xG

def HnearestHG(pH, pG):
	xH, yH = pH
	xH, yH = int(math.floor(xH)), int(math.floor(yH))
	pHs = [(xH + dxH, yH + dyH) for dxH in (0, 1) for dyH in (0, 1)]
	return min(pHs, key = lambda pHnear: math.distance(pG, GconvertH(pHnear)))

def HnearestG(pG):
	return HnearestHG(HconvertG(pG), pG)

def HoutlineH(pH):
	xH, yH = pH
	return [(xH + dxH, yH + dyH) for dxH, dyH in outlinedH]

def GoutlineH(pH):
	return [GconvertH(oH) for oH in HoutlineH(pH)]

@cache
def Hrect(R):
	ret = set()
	for xH in range(-R, R + 1):
		for yH in range(-R, R + 1):
			if abs(xH + yH) <= R:
				ret.add((xH, yH))
	return frozenset(ret)


