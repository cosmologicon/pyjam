from pygame.locals import *
from . import view, state, thing, background

def init():
	state.you = thing.You(x = 0, y = 0)
	state.enemies.append(thing.Medusa(x = 100, y = 0, vx = 20, vy = 5))
	state.enemies.append(thing.Medusa(x = 1000, y = -200, vx = 20, vy = 5))
	state.planets.append(thing.Planet(x = 300, y = -200, name = "Spathiwa"))
	state.planets.append(thing.Planet(x = 400, y = 300, name = "Falayalaralfali"))
	state.planets.append(thing.Planet(x = 1000, y = 100, name = "Unzervalt"))

def think(dt, kdowns, kpressed):
	dx = (kpressed[K_RIGHT] or kpressed[K_d] or kpressed[K_e]) - (kpressed[K_LEFT] or kpressed[K_a])
	dy = (kpressed[K_DOWN] or kpressed[K_s] or kpressed[K_o]) - (kpressed[K_UP] or kpressed[K_w] or kpressed[K_COMMA])
	state.you.move(dt * dx, dt * dy)
	view.think(dt)
	state.think(dt)


def draw():
	background.draw()
	state.draw()

