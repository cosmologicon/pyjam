import math, random
from . import world, thing, graphics
from . import fuzz, ptext, pview
from .pview import T

def init():
	world.generate()
	world.advanceto(1)

def think(dt):
	for obj in world.effects:
		obj.think(dt)
	world.effects = [obj for obj in world.effects if obj.alive]

def draw():
#	pview.fill((0, 0, 0))
	graphics.drawbackground()
	for y in range(pview.h):
		x = int(fuzz.uniform(0, pview.w, 0.432, y))
		c = int(fuzz.uniform(0, 80, 0.543, y) * random.uniform(0.6, 1.5))
		pview.screen.set_at((x, y), (c, c, c))
	alpha = math.interpI(world.maglimit, 1, 255, 6, 0)
	pview.fill((40, 40, 90, alpha))
	for star in world.stars:
		star.draw()
	for link in world.links:
		link.draw()
	for obj in world.effects:
		obj.draw()
	text = f"{world.score}/{len(world.stars)}"
	ptext.draw(text, bottomleft = T(0, 720), owidth = 1, fontsize = T(20), color = "#afafaf")


