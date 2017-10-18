import pygame, math
from . import view

boards = {}
blefts = {}
crosscoords = {}
blocks = []
hills = []
effects = []

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

def think(dt, kdowns, kpressed):
	global youftarget
	kright = (1 if kpressed[pygame.K_RIGHT] else 0) - (1 if kpressed[pygame.K_LEFT] else 0)
	if kright:
		dftarget = 2 * dt * kright
		youftarget = math.clamp(youftarget + dftarget, -1, 1)
	else:
		youftarget = math.softapproach(youftarget, 0, 4 * dt)
	view.X0 += 24 * dt
	you.think(dt)


def youtargetspeed():
	targetx0 = -30 + 15 * youftarget
	x0, _ = view.to0plane(you.x, you.y, you.z)
	dx = targetx0 - x0
	return 24 + 2 * dx

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

