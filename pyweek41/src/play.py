import math
from . import world, thing
from . import fuzz, ptext, pview
from .pview import T

def init():
	world.generate()
	world.advanceto(6)

def think():
	pass

def draw():
	pview.fill((0, 0, 0))
	for y in range(pview.h):
		x = int(fuzz.uniform(0, pview.w, 0.432, y))
		pview.screen.set_at((x, y), (40, 40, 40))
	alpha = math.interpI(world.maglimit, 0, 255, 6, 0)
	pview.fill((40, 40, 90, alpha))
	for star in world.stars:
		star.draw()
	for link in world.links:
		link.draw()
	text = f"{world.score}/{len(world.stars)}"
	ptext.draw(text, bottomleft = T(0, 720), owidth = 1, fontsize = T(20), color = "#afafaf")


