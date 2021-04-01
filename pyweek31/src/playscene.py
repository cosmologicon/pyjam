import random
import pygame
from . import pview, ptext
from . import settings, view, state, thing, hud, levels, scene
from .pview import T

class self:
	pass

class dialog:
	pass

def init():
	state.setspec(levels.data[state.currentlevel])
	dialog.queue = levels.dialog.get(state.currentlevel, [])
	dialog.current = None
	dialog.t = 0
	
	if False:
		while len(state.trees) < 36:
			pH = random.randrange(-8, 9), random.randrange(-8, 9)
			if state.empty(pH):
				state.trees.append(thing.Maple(pH))
	

def control(cstate):
	if "quit" in cstate.kdowns:
		from . import pausescene
		scene.push(pausescene)
		return

	if cstate.scroll:
		view.zoom(cstate.scroll, cstate.mposV)

	if hud.contains(cstate.mposV):
		self.mposH = None
		hud.control(cstate)
		if hud.selected() == "pause":
			from . import pausescene
			scene.push(pausescene)
			hud.self.selected = None
		if hud.selected() == "help":
			from . import helpscene
			scene.push(helpscene)
			hud.self.selected = None
	else:
		self.mposH = view.HconvertV(cstate.mposV)
		if "click" in cstate.events:
			pH = view.HnearesthexH(self.mposH)
			if state.empty(pH):
				selected = hud.selected()
				if selected == "oak":
					state.addtree(thing.Oak(pH, 1))
				if selected == "maple":
					state.addtree(thing.Maple(pH, 1))
				if selected == "elm":
					state.addtree(thing.Oak(pH, 2))
				if selected is not None and len(selected) == 4 and selected[0] == "s" and selected[2] == "-":
					jcolor = int(selected[1])
					jdH = int(selected[3])
					spawner = thing.MultiSpawner(pH, 2, [(jdH, jcolor)])
					state.addspawner(spawner)
				if selected is not None and len(selected) == 4 and selected[0] == "r" and selected[2] == "-":
					jcolor = int(selected[1])
					rH = int(selected[3])
					ring = thing.ChargeRing(pH, jcolor, rH)
					state.addring(ring)
				if selected == "multi":
					jcolors = list(range(len(settings.colors)))
					random.shuffle(jcolors)
					spec = list(zip([-1, 0, 1], jcolors))
					state.addspawner(thing.MultiSpawner(pH, 2, spec))
				if selected == "tri":
					jcolors = list(range(len(settings.colors)))
					random.shuffle(jcolors)
					spec = list(zip([-2, 0, 2], jcolors))
					state.addspawner(thing.MultiSpawner(pH, 2, spec))
					
			elif state.treeat(pH):
				state.treeat(pH).toggle()
			elif state.spawnerat(pH):
				state.spawnerat(pH).toggle()
			elif state.ringat(pH):
				state.ringat(pH).toggle()
		if "rclick" in cstate.events:
			pH = view.HnearesthexH(self.mposH)
			if state.treeat(pH) is not None:
				state.trees.remove(state.treeat(pH))
			if state.ringat(pH) is not None:
				state.rings.remove(state.ringat(pH))
			if state.spawnerat(pH) is not None:
				state.spawners.remove(state.spawnerat(pH))
	if cstate.dragdV is not None:
		view.pan(cstate.dragdV)

def think(dt):
	dialog.t += dt
	if dialog.current is None and dialog.queue:
		dialog.current = dialog.queue.pop(0)
		dialog.t = 0
	elif dialog.current is not None:
		if dialog.t > 2:
			dialog.current = None
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
	if dialog.current:
		text = dialog.current[:5+int(dialog.t * 100)]
		ptext.draw(text, midleft = T(200, 680), fontsize = T(30), owidth = 1)

	hud.draw()

