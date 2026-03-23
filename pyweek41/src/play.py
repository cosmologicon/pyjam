from . import world, thing
from . import fuzz

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

