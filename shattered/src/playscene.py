from __future__ import division
import pygame, math, random
from . import settings, state, thing, background, window, gamedata, control, dialogue, quest, hud
from . import image, scene, mapscene, ptext, sound
from .util import F

curtain = -1

def think(dt, estate):
	global curtain
	control.think(dt, estate)
	dx = 200 * dt * (estate["iskright"] - estate["iskleft"])
	dy = 200 * dt * (estate["iskup"] - estate["iskdown"])
	if dx or dy:
		window.target = None
	window.scoot(dx, dy)
	if estate["map"] and not state.state.final:
		scene.push(mapscene)

#	dialogue.playonce("test1")

	if control.assembling:
		curtain -= 6 * dt
		if curtain < -0.5:
			state.state.assemble(*control.assembling)
			control.assembling = False
			control.cursor = []
	else:
		curtain = min(curtain + 6 * dt, 1)


	hud.clear()
	state.state.think(dt)
	window.think(dt)
	quest.think(dt)
	dialogue.think(dt)
#	window.snapto(state.state.things[-1])
	x, y = window.screentoworld(*estate["mpos"])

	if False:
		if background.revealed(x, y) and background.island(x, y):
			pygame.mouse.set_cursor(*pygame.cursors.arrow)
		else:
			pygame.mouse.set_cursor(*pygame.cursors.broken_x)
	if state.state.final:
		sound.playmusic(1, 1)
	else:
		sound.playmusic(0, 1)
	

def draw():
	background.draw()
	state.state.draw()
#	background.drawclouds()
	dialogue.draw()
	control.drawselection()

	if not state.state.final:
		background.drawminimap()

	avatarrects = [pygame.Rect(F(4 + 64 * j, 4, 60, 60)) for j in range(len(state.state.team))]
	up1rects = [pygame.Rect(F(4 + 64 * j, 68, 28, 28)) for j in range(len(state.state.team))]
	up2rects = [pygame.Rect(F(34 + 64 * j, 68, 28, 28)) for j in range(len(state.state.team))]

	for rect, up1r, up2r, ship in zip(avatarrects, up1rects, up2rects, state.state.team):
		canup1 = ship.up1cost() <= state.state.bank
		canup2 = ship.up2cost() <= state.state.bank
		image.draw(("data/upgrade.png" if canup1 else "data/upgrade-no.png"), up1r.center, size = up1r.width)
		image.draw(("data/upgrade.png" if canup2 else "data/upgrade-no.png"), up2r.center, size = up2r.width)
		if control.isselected(ship):
			window.screen.fill((255, 0, 255), rect)
		else:
			window.screen.fill((0, 0, 0), rect)
		image.draw("avatar-" + ship.letter, rect.center, size = rect.width - F(6))
		for k, charge in enumerate(sorted(ship.chargerates)):
			x, y = rect.center
			x += F((len(ship.chargerates) / 2 - k - 1 / 2) * 14)
			y += F(25)
			color = tuple(settings.ncolors[charge])
			boltinfo = color, None, True
			image.draw("bolt", pos = (x, y), scale = 2.5, boltinfo = boltinfo)
		if rect.collidepoint(*pygame.mouse.get_pos()):
			hud.drawyouinfo(ship.letter)
		if up1r.collidepoint(*pygame.mouse.get_pos()):
			hud.drawup1info(ship.letter, ship.up1cost(), canup1)
		if up2r.collidepoint(*pygame.mouse.get_pos()):
			hud.drawup2info(ship.letter, ship.up2cost(), canup2)
	hud.draw()

	if "credits" in quest.quests:
		quest.quests["credits"].draw()
	if "act3" in quest.quests:
		quest.quests["act3"].draw()

	if curtain <= 0:
		window.screen.fill((0, 0, 0))
	elif curtain < 1:
		h = int(window.sy / 2 * (1 - curtain))
		window.screen.fill((0, 0, 0), (0, 0, window.sx, h))
		window.screen.fill((0, 0, 0), (0, window.sy - h, window.sx, h))

