from __future__ import division
import pygame, math, random
from . import settings, state, thing, background, window, gamedata, control, dialogue, quest, hud
from . import image, scene, mapscene
from .util import F

curtain = -1
def onpush():
	x, y = gamedata.data["start"]
	you = thing.ShipA(pos = [x, y, 4])
	background.reveal(x, y, 40)
	state.state.addtoteam(you)
	state.state.addtoteam(thing.ShipB(pos = [x + 5, y + 5, 3]))
	state.state.addtoteam(thing.ShipC(pos = [x - 5, y - 5, 5]))

#	x, y = gamedata.data["beta"]
#	state.state.addtoteam(thing.BetaShip(pos = [x, y, 4]))

	for j in range(10000):
		x = random.uniform(-1000, 1000)
		y = random.uniform(-1000, 1000)
		state.state.adddecoration(thing.Tree(pos = [x, y, 0]))

	window.snapto(you)
	for x, y in gamedata.data["activated"]:
		building = thing.Building(pos = [x, y, 0], need0 = 10)
		state.state.addbuilding(building)
		

def think(dt, estate):
	global curtain
	control.think(dt, estate)
	dx = 35 * dt * (estate["iskright"] - estate["iskleft"])
	dy = 35 * dt * (estate["iskup"] - estate["iskdown"])
	window.scoot(dx, dy)
	if estate["map"]:
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
	if background.revealed(x, y) and background.island(x, y):
		pygame.mouse.set_cursor(*pygame.cursors.arrow)
	else:
		pygame.mouse.set_cursor(*pygame.cursors.broken_x)

def draw():
	background.draw()
	state.state.draw()
#	background.drawclouds()
	dialogue.draw()
	control.drawselection()

	for j, ship in enumerate(state.state.team):
		pos = F(32 + 64 * j, 32)
		size = F(60)
		image.draw("avatar-" + ship.letter, pos, size = size)
		if control.isselected(ship):
			rect = pygame.Rect(0, 0, size, size)
			rect.center = pos
			pygame.draw.rect(window.screen, (255, 0, 255), rect, F(3))
	hud.draw()

	quest.quests["credits"].draw()

	if curtain <= 0:
		window.screen.fill((0, 0, 0))
	elif curtain < 1:
		h = int(window.sy / 2 * (1 - curtain))
		window.screen.fill((0, 0, 0), (0, 0, window.sx, h))
		window.screen.fill((0, 0, 0), (0, window.sy - h, window.sx, h))

