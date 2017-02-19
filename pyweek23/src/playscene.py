import math
from pygame.locals import *
from . import view, state, thing, background, settings, hud

def init():
	state.you = thing.You(x = 0, y = 0)
	state.yous.append(state.you)
	state.yous.append(thing.Companion(x = 0, y = 0))
#	state.addmedusa(300, 0)
	state.addwave(700, 0, 4, 6, [
		[0, 350, 0],
		[3, 200, 200],
		[6, 0, -200],
		[9, -600, 0],
	])
	state.addrockwave(900, 0, 60, 200)
	state.pickups.append(thing.MissilesPickup(x = 300, y = 0))
	state.planets.append(thing.Planet(x = 300, y = -200, name = "Spathiwa"))
	state.planets.append(thing.Planet(x = 400, y = 300, name = "Falayalaralfali"))
	state.planets.append(thing.Planet(x = 1000, y = 100, name = "Unzervalt"))

def think(dt, kdowns, kpressed):
	if settings.isdown("swap", kdowns):
		settings.swapaction = not settings.swapaction
	dx = settings.ispressed("right", kpressed) - settings.ispressed("left", kpressed)
	dy = settings.ispressed("down", kpressed) - settings.ispressed("up", kpressed)
	if dx and dy:
		dx *= math.sqrt(0.5)
		dy *= math.sqrt(0.5)
	state.you.move(dt * dx, dt * dy)
	if settings.ispressed("action", kpressed) != settings.swapaction:
		state.you.act()
	view.think(dt)
	state.think(dt)


def draw():
	background.draw()
	state.draw()
	hud.draw()

