import pygame
from . import settings, state, thing, background, window, gamedata, control
from .util import F

curtain = -1
def onpush():
	x, y = gamedata.data["start"]
	you = thing.AlphaShip(pos = [x, y, 4])
	background.reveal(x, y, 15)
	state.state.addtoteam(you)
	x, y = gamedata.data["beta"]
	state.state.addtoteam(thing.BetaShip(pos = [x, y, 4]))
	window.snapto(you)
	for x, y in gamedata.data["activated"]:
		building = thing.Building(pos = [x, y, 0], needpower = 10)
		state.state.addbuilding(building)

def think(dt, estate):
	global curtain
	control.think(dt, estate)

	if control.assembling:
		curtain -= 6 * dt
		if curtain < -0.5:
			state.state.assemble(window.x0, window.y0)
			control.assembling = False
			control.cursor = []
	else:
		curtain = min(curtain + 6 * dt, 1)

	state.state.think(dt)
	window.think(dt)
#	window.snapto(state.state.things[-1])

def draw():
	background.draw()
	state.state.draw()
#	background.drawclouds()
	control.drawselection()
	if curtain <= 0:
		window.screen.fill((0, 0, 0))
	elif curtain < 1:
		h = int(window.sy / 2 * (1 - curtain))
		window.screen.fill((0, 0, 0), (0, 0, window.sx, h))
		window.screen.fill((0, 0, 0), (0, window.sy - h, window.sx, h))

	for j, ship in enumerate(state.state.team):
		rect = pygame.Rect(F(0, 0, 60, 60))
		rect.center = F(32 + 64 * j, 32)
		color = (200, 0, 200) if control.isselected(ship) else (60, 60, 60)
		window.screen.fill(color, rect)


