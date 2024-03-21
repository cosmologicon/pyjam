import math
from functools import cache
from itertools import cycle, chain
from . import state, grid


colorcosts = [1, 1, 1, 2, 2, 3]

@cache
def colorsets(cost, j0 = 0):
	if cost == 0:
		return [[]]
	if j0 >= len(colorcosts):
		return []
	ret = list(colorsets(cost, j0 + 1))
	if colorcosts[j0] <= cost:
		ret += [[j0] + cset for cset in colorsets(cost - colorcosts[j0], j0 + 1)]
	return ret

def randomplanet(hasvalue, needsvalue, *seed):
	for j in range(10000):
		has = math.fuzzchoice(colorsets(hasvalue), j, 101, *seed)
		needs = math.fuzzchoice(colorsets(needsvalue), j, 102, *seed)
		if not(set(has) & set(needs)):
			return [
				{ settings.colors[x]: 1 for x in has },
				{ settings.colors[x]: 1 for x in needs },
			]

def spiral():
	for j in range(4, 100):
		pG = math.CS(j * math.phyllo, r = 1.5 * math.sqrt(j))
		pH = grid.HnearestG(pG)
		hasvalue = int(math.interp(j, 1, 1, 60, 4))
		needsvalue = int(math.interp(j, 1, 1, 80, 4))
#		state.addrandomplanet(pH, ncolor, nhas, nneeds)
		has, needs = randomplanet(hasvalue, needsvalue, j)
		state.addplanet(pH, has = has, needs = needs)

def addcentral():
	state.addplanet((0, 1), supply = "R")
	state.addplanet((1, -1), supply = "O")
	state.addplanet((-1, 0), supply = "Y")

def getspots(pHs):
	spots = []
	for pH in pHs:
		if not state.isfree(pH): continue
		if not all(state.isfree(pHadj) for pHadj in grid.HadjsH(pH)): continue
		if any(state.planetat(pHadj) for pHadj in grid.HadjsH(pH)):
			continue
		if not all(nvisible(pHadj) for pHadj in grid.HadjsH(pH)):
			continue
		if any(grid.isadjH(pH, claimed) for claimed in spots):
			continue
		spots.append(pH)
	return spots

def assign(spots, tranches, tranche0 = []):
	j0 = 0
	for tranche in chain([tranche0], cycle(tranches)):
		if j0 + len(tranche) > len(spots):
			return
		for opt in tranche:
			yield spots[j0], opt
			j0 += 1

def addrocks(frac, *seed):
	for pH in state.board:
		if state.isfree(pH) and not any(state.planetat(pHadj) for pHadj in grid.HadjsH(pH)):
			if math.fuzz(500, *pH, *seed) < frac:
				state.addrock(pH)

@cache
def noisegrid0(px, py, *seed):
	return math.fuzzrange(-1, 1, 700, px % 16, py % 16, *seed)

@cache
def noisegrid(x, y, *seed):
	nx, fx = divmod(x, 1)
	ny, fy = divmod(y, 1)
	noise00 = noisegrid0(nx, ny, 701, *seed)
	noise01 = noisegrid0(nx, ny + 1, 701, *seed)
	noise10 = noisegrid0(nx + 1, ny, 701, *seed)
	noise11 = noisegrid0(nx + 1, ny + 1, 701, *seed)
	noise0 = math.mix(noise00, noise10, fx)
	noise1 = math.mix(noise01, noise11, fx)
	return math.mix(noise0, noise1, fy)
	

@cache
def noise(pG, *seed):
	x, y = pG
	ret = 0
	f = 1
	x *= 0.2
	y *= 0.2
	for j in range(14):
		x += math.fuzzrange(0, 100, 706, *seed)
		y += math.fuzzrange(0, 100, 707, *seed)
		x *= 1.3
		y *= 1.3
		ret += f * noisegrid(x, y, 705, *seed)
		f /= 1.4
	return ret

def nvisible(pH):
	rG = math.length(grid.GconvertH(pH))
#	return noise(grid.GconvertH(pH), 712) > -0.3
	return math.fuzz(*pH, 713) > math.interp(rG, 5, 0, 18, 0.3)


def revealto(R):
	state.setvisibility(R)
	for pH in list(state.visible):
		if not nvisible(pH):
			state.addrock(pH)
#			state.visible.remove(pH)

def phase(R, seed, opts0, opts, planetmax):
	visible0 = set(state.visible)
	revealto(R)
	pHs = math.fuzzshuffle(sorted(set(state.visible) - visible0), seed)
	for pH, spec in assign(getspots(pHs), opts, opts0):
		demand, supply = spec.split(",")
		state.addplanet(pH, supply, demand)
		if len(state.planets) >= planetmax:
			break
	print(len(state.planets))
	state.resolvenetwork()
	

def phase1():
	addcentral()
	opts = [
		["R,O", "O,R"],
		["O,Y", "Y,O"],
		["R,Y", "Y,R"],
	]
	phase(6, 101, [], opts, 15)

def phase2():
	opts0 = ["G,RY", "R,G", "Y,G"]  # +1G
	opts = [
		["G,RY", "RY,G"],
		["G,O", "O,G"],
		["G,OR", "OR,G"],
		["G,Y", "Y,G"],
		["G,OY", "OY,G"],
		["G,R", "R,G"],
		["R,O", "O,R"],
		["O,Y", "Y,O"],
		["R,Y", "Y,R"],
	]
	phase(8.5, 211, opts0, opts, 30)
	
def phase3():
	opts0 = ["B,OY", "O,B", "Y,G", "G,B"]  # +1B
	opts = [
		["B,G", "G,B"],
		["G,RY", "RY,G"],
		["B,O", "O,B"],
		["B,OR", "OR,B"],
		["G,Y", "Y,G"],
		["G,OY", "OY,G"],
		["B,R", "R,B"],
		["B,RY", "RY,B"],
		["G,O", "O,G"],
		["G,OR", "OR,G"],
		["B,Y", "Y,B"],
		["B,OY", "OY,B"],
		["G,R", "R,G"],
		["BY,GO", "BR,GY", "GO,BR", "G,B"],
		["BO,GR", "GY,BO", "GR,BY", "B,G"],
	]
	phase(13.0, 303, opts0, opts, 46)

def ezphase1():
	addcentral()
	opts0 = ["R,OY", "Y,OR", "O,YR"]
	opts = [
		["R,O", "O,R"],
		["O,Y", "Y,O"],
		["R,Y", "Y,R"],
	]
	phase(6.8, 402, opts0, opts, 12)

def ezphase2():
	visible0 = set(state.visible)
	opts0 = ["G,RY", "R,G", "Y,G", "G,RO", "R,G", "O,G", "G,OY", "O,G", "Y,G"]  # +3G
	opts = [
		["R,O", "O,R"],
		["O,Y", "Y,O"],
		["R,Y", "Y,R"],
	]
	phase(10.5, 502, opts0, opts, 27)

def ezphase3():
	opts0 = ["B,RY", "R,B", "Y,B", "B,RO", "R,B", "O,B", "B,OY", "O,B", "Y,B"]  # +3B
	opts = [
		["B,G", "G,B"],
	]
	phase(16.5, 602, opts0, opts, 38)
	


def tutorial1():
	state.addvisibility(3, (-2, 1))
	state.addvisibility(3, (2, -1))
	state.addplanet((-2, 1), demand = "", supply = "R")
	state.addplanet((2, -1), demand = "R", supply = "O")
	state.resolvenetwork()

def tutorial2():
	state.addvisibility(4, (0, 4))
	state.addplanet((0, 6), demand = "O", supply = "Y")
	state.addplanet((2, 2), demand = "Y", supply = "R")
	state.addplanet((-2, 4), demand = "R", supply = "G")
	state.resolvenetwork()

def tutorial3():
	state.addvisibility(4, (-4, 5))
	state.addplanet((-5, 7), demand = "G", supply = "O")
	state.addplanet((-6, 9), demand = "O", supply = "Y")
	state.addplanet((-5, 4), demand = "Y")
	state.addrock((-7, 7))
	state.addrock((-6, 7))
	state.addrock((-4, 7))
	state.addrock((-3, 7))
	state.resolvenetwork()


def tutorial4():
	state.addvisibility(4.5, (6, 2))
	state.addplanet((6, 2), demand = "ROY", supply = "GB")
	state.addplanet((5, 1), demand = "", supply = "R")
	state.addplanet((5, 4), demand = "", supply = "O")
	state.addplanet((8, 1), demand = "", supply = "Y")
	state.addplanet((7, 0), demand = "G", supply = "")
	state.addplanet((7, 3), demand = "B", supply = "")
	state.resolvenetwork()


def tutorial5():
	state.addvisibility(8.5, (12, -9))
	state.addplanet((8, -4), demand = "", supply = "RRR")
	state.addplanet((12, -6), demand = "", supply = "OOO")
	state.addplanet((16, -8), demand = "", supply = "YYY")
	state.addplanet((8, -10), demand = "ROY", supply = "")
	state.addplanet((12, -12), demand = "ROY", supply = "")
	state.addplanet((16, -14), demand = "ROY", supply = "")
	state.resolvenetwork()


if __name__ == "__main__":
	import pygame
	from . import pview, maff
	pygame.display.init()
	px, py = 400, 400
	pview.set_mode((px, py))
	for x in range(px):
		for y in range(py):
			pG = x / 10, y / 10
			print(noise(pG))
			c = int(math.interp(noise(pG), -2, 0, 2, 255))
			if c < 112: c = 20
			pview.screen.set_at((x, y), (c, c, c, 255))
	pygame.display.flip()
	while not any(event.type == pygame.QUIT for event in pygame.event.get()):
		pass
	



