import math, random
from . import world, thing, graphics
from . import fuzz, ptext, pview
from .pview import T

def init():
	world.generate()
	world.advanceto(1)
	world.sky = 0

def think(dt):
	for obj in world.effects:
		obj.think(dt)
	world.effects = [obj for obj in world.effects if obj.alive]
	world.sky = math.approach(world.sky, world.maglimit, 1 * dt)

def draw():
	graphics.drawback(world.sky)
	for star in world.stars:
		star.draw()
	for link in world.links:
		link.draw()
	for obj in world.effects:
		obj.draw()
	graphics.drawtreeline()
	text = f"{world.score}/{len(world.stars)}"
	ptext.draw(text, bottomleft = T(0, 720), owidth = 1, fontsize = T(20), color = "#afafaf")


