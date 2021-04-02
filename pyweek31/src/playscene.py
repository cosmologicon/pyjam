import random, math
import pygame
from . import pview, ptext
from . import settings, view, state, thing, hud, levels, scene, progress, graphics
from .pview import T

class self:
	pass

class dialog:
	pass

def init():
	state.R = levels.R.get(state.currentlevel, 17.4)
	state.setspec(levels.data[state.currentlevel])
	dialog.queue = levels.dialog.get(state.currentlevel, [])
	dialog.current = None
	dialog.t = 0
	self.twin = 0
	self.won = False
	

def control(cstate):
	if "quit" in cstate.kdowns:
		from . import pausescene
		scene.push(pausescene)
		return

	if cstate.scroll:
		view.zoom(cstate.scroll, cstate.mposV)

	hud.control(cstate)
	if hud.contains(cstate.mposV):
		self.mposH = None
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
			if state.canbuildat(pH):
				selected = hud.selected()
				if selected == "oak":
					state.addtree(thing.Oak(pH, 1))
				if selected == "beech":
					state.addtree(thing.Beech(pH, 1))
				if selected == "pine":
					state.addtree(thing.Pine(pH, 2))
				if selected is not None and len(selected) == 4 and selected[0] == "s" and selected[2] == "-":
					jcolor = int(selected[1])
					jdH = int(selected[3])
					spawner = thing.Spawner(pH, 2, [(jdH, jcolor)])
					state.addspawner(spawner)
				if selected is not None and len(selected) == 4 and selected[0] == "r" and selected[2] == "-":
					jcolor = int(selected[1])
					rH = int(selected[3])
					ring = thing.Ring(pH, jcolor, rH)
					state.addring(ring)
				if selected == "multi":
					jcolors = list(range(len(settings.colors)))
					random.shuffle(jcolors)
					spec = list(zip([-1, 0, 1], jcolors))
					state.addspawner(thing.Spawner(pH, 2, spec))
				if selected == "tri":
					jcolors = list(range(len(settings.colors)))
					random.shuffle(jcolors)
					spec = list(zip([-2, 0, 2], jcolors))
					state.addspawner(thing.Spawner(pH, 2, spec))
					
			elif state.treeat(pH):
				state.treeat(pH).toggle()
			elif state.spawnerat(pH):
				state.spawnerat(pH).toggle()
			elif state.ringat(pH):
				state.ringat(pH).toggle()
		if "rclick" in cstate.events:
			pH = view.HnearesthexH(self.mposH)
			if state.treeat(pH) is not None:
				state.removetree(pH)
			if settings.DEBUG and state.ringat(pH) is not None:
				state.removering(pH)
			if settings.DEBUG and state.spawnerat(pH) is not None:
				state.removespawner(pH)
	self.dragging = cstate.dragdV is not None
	if self.dragging:
		view.pan(cstate.dragdV)

def think(dt):
	dialog.t += dt
	if not self.dragging:
		view.snap(dt)
	if dialog.current is None and dialog.queue:
		dialog.current = dialog.queue.pop(0)
		dialog.t = 0
	elif dialog.current is not None:
		if dialog.t > 2:
			dialog.current = None
	for tree in state.trees:
		tree.think(dt)
	for spawner in state.spawners:
		spawner.think(dt)
	for ghost in state.ghosts:
		ghost.think(dt)
	for bug in state.bugs:
		bug.think(dt)
	state.ghosts = [ghost for ghost in state.ghosts if ghost.alive]
	state.bugs = [bug for bug in state.bugs if bug.alive]
	for ring in state.rings:
		ring.think(dt)
	winning = all(ring.charged() for ring in state.rings)
	if winning:
		self.twin += dt
	if winning and self.twin > 5:
		win()


def win():
	if self.won:
		return
	self.won = True
	progress.beaten.add(state.currentlevel)
	for level in levels.unlocks.get(state.currentlevel, []):
		progress.unlocked.add(level)
	scene.pop()

def draw():
	graphics.drawground()
	if False:
		for pH in state.grid0:
			if state.canbuildat(pH):
				for j in range(6):
					pV0 = view.VconvertH(view.vecadd(pH, view.HrotH((1, 1), j), 1/3))
					pV1 = view.VconvertH(view.vecadd(pH, view.HrotH((1, 1), j + 1), 1/3))
					pygame.draw.line(pview.screen, (70, 140, 70), pV0, pV1, 1)
	if self.mposH is not None and hud.selected():
		pH = view.HnearesthexH(self.mposH)
		if pH in state.grid0:
			color = (80, 20, 20) if pH in state.taken else (60, 60, 60)
			pVs = [view.VconvertH(view.vecadd(pH, dH)) for dH in view.cornerdHs]
			pygame.draw.polygon(pview.screen, color, pVs)
	for tree in state.trees:
		tree.drawroots()
	for ring in state.rings:
		ring.draw()
	for spawner in state.spawners:
		spawner.draw()
	for tree in state.trees:
		tree.draw()
	for ghost in state.ghosts:
		ghost.draw()
	for bug in state.bugs:
		bug.draw()

	graphics.drawshades()

	if dialog.current:
		text = dialog.current[:5+int(dialog.t * 100)]
		ptext.draw(text, midleft = T(200, 680), fontsize = T(30), owidth = 1)
	else:
		ncharge = sum(ring.charged() for ring in state.rings)
		ptext.draw("MAGIC: %d/%d" % (ncharge, len(state.rings)), bottomleft = T(20, 700),
			fontsize = T(60), owidth = 0.5, ocolor = (255, 128, 128), color = "red", shade = 1)

	hud.draw()


	if settings.DEBUG:
		graphics.reportcache()


