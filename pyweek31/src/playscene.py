import random
import pygame
from . import pview
from . import settings, view, state, thing, hud

class self:
	pass

def init():
	if False:
		state.bugs = []
		state.rings = []
		state.spawners = [
			thing.BugSpawner((0, -8), (0, 1), thing.Ant, settings.colors[0], 2.2),
		]
		state.trees = []
	if False:
		while len(state.trees) < 36:
			pH = random.randrange(-8, 9), random.randrange(-8, 9)
			if state.empty(pH):
				state.trees.append(thing.Maple(pH))
	

def control(mposV, events):
	if hud.contains(mposV):
		self.mposH = None
		hud.control(mposV, events)
	else:
		self.mposH = view.HconvertV(mposV)
		if "click" in events:
			pH = view.HnearesthexH(self.mposH)
			if state.empty(pH):
				ttype = None
				selected = hud.selected()
				if selected == "oak":
					ttype = thing.Oak
				if selected == "maple":
					ttype = thing.Maple
				if ttype is not None:
					state.trees.append(ttype(pH))
				if selected is not None and selected.startswith("ring"):
					color = settings.colors[int(selected[-1])]
					state.rings.append(thing.ChargeRing(pH, color))
		if "rclick" in events:
			pH = view.HnearesthexH(self.mposH)
			if state.treeat(pH) is not None:
				state.trees.remove(state.treeat(pH))
			if state.ringat(pH) is not None:
				state.rings.remove(state.ringat(pH))
			if state.spawnerat(pH) is not None:
				state.spawners.remove(state.spawnerat(pH))
			

def think(dt):
	for spawner in state.spawners:
		spawner.think(dt)
	for bug in state.bugs:
		bug.think(dt)
	state.bugs = [bug for bug in state.bugs if bug.alive]
	for ring in state.rings:
		ring.think(dt)

def draw():
	for pG0, pG1 in view.gridedgeGs:
		pygame.draw.line(pview.screen, (70, 140, 70), view.VconvertG(pG0), view.VconvertG(pG1), 1)
	if self.mposH is not None:
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
	hud.draw()

