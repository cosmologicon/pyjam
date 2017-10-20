import pygame, math
from . import view, settings

def reset():
	global boards, blefts, crosscoords, blocks, hills, effects, hazards, you, youftarget
	boards = {}
	blefts = {}
	crosscoords = {}
	blocks = []
	hills = []
	effects = []
	hazards = []
	youftarget = 0

def addboard(board):
	boards[board.name] = board
	blefts[(board.x, board.y, board.z)] = board

def lastboard():
	return max(boards.values(), key = lambda board: view.cameraat0(board.x, board.z, 0))

def addhill(hill):
	for board in hill.boards():
		addboard(board)
	blocks.append(hill.block())
	hills.append(hill)

def blockedat0(p0, z):
	return any(block.z > z and block.contains0(p0) for block in blocks)


def think(dt, kdowns, kpressed):
	global youftarget, boards, blocks, hills, effects
	kright = (1 if kpressed[pygame.K_RIGHT] else 0) - (1 if kpressed[pygame.K_LEFT] else 0)
	if kright:
		dftarget = 2 * dt * kright
		youftarget = math.clamp(youftarget + dftarget, -1, 1)
	else:
		youftarget = math.softapproach(youftarget, 0, 4 * dt)
	view.X0 += settings.speed * dt
	you.think(dt)
	for hazard in hazards:
		hazard.think(dt)
	removegone()
	for hazard in hazards:
		if hazard.hitsyou():
			you.gethit()

def removegone():
	global boards, blocks, hills, hazards, effects
	nboards = {}
	for boardname, board in boards.items():
		if board.gone():
			del blefts[(board.x, board.y, board.z)]
		else:
			nboards[boardname] = board
	boards = nboards
	blocks = [block for block in blocks if not block.gone()]
	hills = [h for h in hills if not h.gone()]
	hazards = [h for h in hazards if not h.gone()]
	effects = [effect for effect in effects if effect.alive()]

def youtargetspeed():
	targetx0 = -settings.lag + 10 * youftarget
	x0, _ = view.to0plane(you.x, you.y, you.z)
	dx = targetx0 - x0
	return settings.speed + 2 * dx

def resolve():
	global crosscoords, crossings
	p0 = view.to0plane(you.x, you.y, you.z)
	newcrosscoords = { name: board.crosspos(p0) for name, board in boards.items() }
	crossings = []
	for name, (a1, b1) in newcrosscoords.items():
		if name not in crosscoords:
			continue
		a0, b0 = crosscoords[name]
		if b0 > 0 and b1 <= 0:
			crossings.append((name, a0, b0, a1, b1))
	crosscoords = newcrosscoords
	you.resolve()

def losing():
	return you.y < -30

# Return the camera position X0 at which all hills will be left of the given x0 position on the
# screen. e.g. x0 = 0 means all hills currently in the state will be left of the center.
def endingX0at(x0):
	return max(
		view.cameraat0(h.hilltopend()[0], h.z, x0)
		for h in hills
	)


