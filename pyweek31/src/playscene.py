import random, math
import pygame
from . import pview, ptext
from . import settings, view, state, thing, hud, levels, scene, progress, graphics, sound
from .pview import T

class self:
	pass

class dialog:
	pass

def init():
	state.R = levels.R.get(state.currentlevel, 17.4)
	if state.currentlevel not in progress.seen:
		dialog.queue = levels.dialog.get(state.currentlevel, [])
	else:
		dialog.queue = []
	dialog.current = None
	dialog.t = 0
	self.t = 0
	self.twin = 0
	self.won = False
	hud.reset()
	view.reset()	

def control(cstate):
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
		pH = view.HnearesthexH(self.mposH)
		if settings.DEBUG and "act" in cstate.kdowns:
			if state.spawnerat(pH):
				state.spawnerat(pH).rotate()
			if state.ringat(pH):
				state.ringat(pH).toggle()
		if "click" in cstate.events:
			if state.canbuildat(pH):
				selected = hud.selected()
				if selected == "oak":
					state.addtree(thing.Oak(pH, 1))
					sound.playsound("grow0")
				if selected == "beech":
					state.addtree(thing.Beech(pH, 1))
					sound.playsound("grow1")
				if selected == "pine":
					state.addtree(thing.Pine(pH, 2))
					sound.playsound("grow2")
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
				sound.playsound("swap")
			elif state.spawnerat(pH):
				state.spawnerat(pH).toggle()
				sound.playsound("chime")
			else:
				sound.playsound("no")
		if "rclick" in cstate.events:
			pH = view.HnearesthexH(self.mposH)
			if state.treeat(pH) is not None:
				state.removetree(pH)
				sound.playsound("ungrow")
			if settings.DEBUG and state.ringat(pH) is not None:
				state.removering(pH)
			if settings.DEBUG and state.spawnerat(pH) is not None:
				state.removespawner(pH)
	self.dragging = cstate.dragdV is not None
	if self.dragging:
		view.pan(cstate.dragdV)

def think(dt):
	self.t += dt
	dialog.t += dt
	if not self.dragging:
		view.snap(dt)
	if dialog.current is None and dialog.queue and self.t > 1:
		dialog.current = dialog.queue.pop(0)
		dialog.t = 0
	elif dialog.current is not None:
		if dialog.t > len(dialog.current) / 40 + 3:
			dialog.current = None
			if not dialog.queue:
				progress.seen.add(state.currentlevel)
				progress.save()
	if dialog.current and dialog.t * 60 < len(dialog.current):
		if 0.05 * random.random() < dt:
			sound.playsound("yak%d" % random.choice([0, 1, 2, 3, 4]))
	
	dt *= settings.speed
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
	winning = all(ring.charged() for ring in state.rings) and state.currentlevel != "empty"
	if winning or self.twin > 4:
		self.twin += dt
		if self.twin <= 4 < self.twin + dt:
			sound.playsound("win")
	if self.twin > 6:
		win()


def win():
	if self.won:
		return
	self.won = True
	progress.beaten.add(state.currentlevel)
	for level in levels.unlocks.get(state.currentlevel, []):
		progress.unlocked.add(level)
	state.reset()
	progress.save()
	scene.pop()

def draw():
	graphics.drawground()
	if self.mposH is not None and hud.selected():
		pH = view.HnearesthexH(self.mposH)
		if pH in state.grid0:
			color = (80, 20, 20) if pH in state.taken else (60, 60, 60)
			pVs = [view.VconvertH(view.vecadd(pH, dH)) for dH in view.cornerdHs]
			pygame.draw.polygon(pview.screen, color, pVs)
			if pH not in state.taken and hud.selected() in ["oak", "beech", "pine"]:
				rG = {
					"oak": thing.Oak.rG,
					"beech": thing.Beech.rG,
					"pine": thing.Pine.rG,
				}[hud.selected()]
				scale = view.VscaleG(rG * 20) / 4000
				graphics.drawimg(view.VconvertH(pH), hud.selected(), scale = scale, cmask = (255, 255, 255, 100))
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
		s = round(1 + 0.05 * math.cycle(10 * dialog.t), 2) if dialog.t * 60 < len(dialog.current) else 1
		graphics.drawimg(T(140, 600), "gnorman", scale = 0.4 * s * pview.f, xscale = 1 / s ** 2)
		text = dialog.current[:5+int(dialog.t * 60)]
		ptext.draw(text, midleft = T(280, 600), width = T(800),
			fontsize = T(50), color = (100, 200, 100), shade = 1, owidth = 0.5)
	else:
		ncharge = sum(ring.charged() for ring in state.rings)
		ptext.draw("Rings: %d/%d" % (ncharge, len(state.rings)), bottomleft = T(15, 720),
			fontsize = T(60), owidth = 1, color = (50, 200, 50), shade = 1)
		if state.currentlevel in levels.tutorial and not dialog.queue:
			text = "\n".join(levels.tutorial[state.currentlevel])
			ptext.draw(text, bottomleft = T(440, 710), fontname = "Londrina",
				fontsize = T(24), owidth = 1, color = (100, 200, 100), shade = 1)
			

	hud.draw()


	if settings.DEBUG:
		graphics.reportcache()


