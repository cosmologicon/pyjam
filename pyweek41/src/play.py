import math, random
from . import world, thing, graphics, quest, control, sound
from . import fuzz, ptext, pview
from .pview import T

def init():
	world.generate()
	world.advanceto(1)
	world.sky = 1
	quest.init()

def think(dt):
	for obj in world.effects:
		obj.think(dt)
	world.effects = [obj for obj in world.effects if obj.alive]
	world.sky = math.approach(world.sky, world.maglimit, 0.2 * dt)
	quest.think(dt)

def draw():
	graphics.drawback(world.sky)
	graphics.drawlinks()
	for star in world.stars.values():
		star.draw()
	graphics.coverstars(world.sky)
	for obj in world.effects:
		obj.draw()
	graphics.drawtreeline()
	control.draw()
	quest.draw()


