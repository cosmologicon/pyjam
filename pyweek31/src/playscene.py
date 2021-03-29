import random
import pygame
from . import pview
from . import view, state, thing

class self:
	pass

def init():
	state.bugs = []
	state.rings = [thing.ChargeRing((0, 0))]
	state.spawners = [
		thing.BugSpawner((0, -8), (0, 1), thing.Ant, 3),
		thing.BugSpawner((-8, 1), (1, 0), thing.Ant, 3),
		thing.BugSpawner((-8, 7), (1, -1), thing.Ant, 3),
	]
	state.trees = []
	while len(state.trees) < 36:
		pH = random.randrange(-8, 9), random.randrange(-8, 9)
		if state.empty(pH):
			state.trees.append(thing.Maple(pH))
	self.tbug = 1
	

def control(mposV, events):
	self.mposH = view.HconvertV(mposV)
	if "click" in events:
		pH = view.HnearesthexH(self.mposH)
		if not state.treeat(pH):
			state.trees.append(thing.Oak(pH))
		

def think(dt):
	for spawner in state.spawners:
		spawner.think(dt)
	for bug in state.bugs:
		bug.think(dt)
	state.bugs = [bug for bug in state.bugs if bug.alive]
	for ring in state.rings:
		ring.think(dt)

def draw():
	for xH in range(-3, 4):
		for yH in range(-3, 4):
			pVs = [view.VconvertH(view.vecadd((xH, yH), dH)) for dH in view.cornerdHs]
			for j in range(6):
				pygame.draw.line(pview.screen, (100, 200, 100), pVs[j], pVs[(j+1)%6], 1)
	pH = view.HnearesthexH(self.mposH)
	pVs = [view.VconvertH(view.vecadd(pH, dH)) for dH in view.cornerdHs]
	pygame.draw.polygon(pview.screen, (40, 80, 40), pVs)
	for ring in state.rings:
		ring.draw()
	for spawner in state.spawners:
		spawner.draw()
	for tree in state.trees:
		tree.draw()
	for bug in state.bugs:
		bug.draw()

