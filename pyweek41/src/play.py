from . import world, thing
from . import fuzz, ptext
from .pview import T

def init():
	world.generate()
	world.advanceto(2)

def think():
	pass

def draw():
	for star in world.stars:
		star.draw()
	for link in world.links:
		link.draw()
	text = f"{world.score}/{len(world.stars)}"
	ptext.draw(text, bottomleft = T(0, 720), owidth = 1, fontsize = T(20), color = "#afafaf")


