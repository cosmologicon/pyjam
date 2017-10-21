# Game state module keeps track of game objects.

import pygame, math
from . import view, settings

def reset():
	global boards, blefts, crosscoords, blocks, hills, effects, hazards, you, youftarget
	# Boards are linear spans you can run across. The top layer of every hill is made up of a series
	# of boards. Boards are stored by "name", a hashable representation of their position in the
	# game world.
	boards = {}
	# Left edges of every board. This is used for the handoff algorithm. When the player runs off
	# the right side of a board, a board whose left edge is at the exact same position (including
	# z-coordinate) can pick them up.
	blefts = {}
	# For the purposes of collision detection, we keep track of the player position with respect to
	# every board each frame. A player may land on a board if they're above it one one frame and
	# below it on the next frame (as well as some other conditions, of course).
	crosscoords = {}
	# Blocks are polygonal objects that remove from existence anything behind them, specifically
	# hazards and boards. Every hill has a board corresponding to its outline.
	blocks = []
	# The hill objects are kept here for drawing. Their interaction with the game world is already
	# handled when their corresponding boards and blocks are added.
	hills = []
	# Extra effects, specifically text and mist.
	effects = []
	# Hazards that can hurt you.
	hazards = []
	# Specifies where on the screen the player character would like to get to. Ranges from -1 to 1,
	# depending on how long left and right have been held down.
	youftarget = 0

def addboard(board):
	boards[board.name] = board
	blefts[(board.x, board.y, board.z)] = board

# Rightmost edge of the rightmost board. Used to determine where to start the next challenge
# segment.
def lastboard():
	return max(boards.values(), key = lambda board: view.cameraat0(board.x, board.z, 0))

# Also add the corresponding boards and block.
def addhill(hill):
	for board in hill.boards():
		addboard(board)
	blocks.append(hill.block())
	hills.append(hill)

# Is the given point (projected onto the z = 0 plane) blocked by any block with a greater z-value
# than z?
def blockedat0(p0, z):
	return any(block.z > z and block.contains0(p0) for block in blocks)


def think(dt, kdowns, kpressed):
	global youftarget, boards, blocks, hills, effects
	kright = (1 if settings.ispressed(kpressed, "right") else 0) - (1 if settings.ispressed(kpressed, "left") else 0)
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

# Player speed is determined by how far off the player is from their target position.
def youtargetspeed():
	targetx0 = -settings.lag + 10 * youftarget
	x0, _ = view.to0plane(you.x, you.y, you.z)
	dx = targetx0 - x0
	return settings.speed + 2 * dx

# Called after think. This handles collision detection.
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


