import random
import pygame
from . import pview
from . import view, state, thing

class self:
	pass

def init():
	state.bugs = []
	state.trees = [
		thing.Maple((random.randrange(-3, 4), random.randrange(-1, 4)))
		for _ in range(6)
	]
	self.tbug = 1
	

def control(mposV):
	self.mposH = view.HconvertV(mposV)

def think(dt):
	self.tbug += dt
	if self.tbug >= 1:
		self.tbug -= 1
		state.bugs.append(thing.Ant((random.randrange(-3, 4), -3), (0, 1)))
	for bug in state.bugs:
		bug.think(dt)

def draw():
	for xH in range(-3, 4):
		for yH in range(-3, 4):
			pVs = [view.VconvertH(view.vecadd((xH, yH), dH)) for dH in view.cornerdHs]
			for j in range(6):
				pygame.draw.line(pview.screen, (100, 200, 100), pVs[j], pVs[(j+1)%6], 1)
	pH = view.HnearesthexH(self.mposH)
	pVs = [view.VconvertH(view.vecadd(pH, dH)) for dH in view.cornerdHs]
	pygame.draw.polygon(pview.screen, (40, 80, 40), pVs)
	for tree in state.trees:
		tree.draw()
	for bug in state.bugs:
		bug.draw()

