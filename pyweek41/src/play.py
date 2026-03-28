import math, random
from . import world, thing, graphics, quest, control, sound, settings
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

def draw(capture = False):
	graphics.drawback(world.sky)
	graphics.drawlinks()
	for star in world.stars.values():
		star.draw(capture)
	graphics.coverstars(world.sky)
	if not capture:
		for obj in world.effects:
			obj.draw()
	graphics.drawtreeline()
	if not capture:
		control.draw()
		quest.draw()
	alpha = math.interp(world.sky, 1, 0.3, 1.5, 0)
	if alpha > 0:
		ptext.ALPHA_RESOLUTION = 256
		ptext.draw(settings.gamename, center = T(200, 100), angle = 10, alpha = alpha,
			color = "#ffafff", owidth = 0.3, shade = 1, shadow = (0.3, 0.3),
			fontsize = T(80), fontname = "Quintessential")
		ptext.ALPHA_RESOLUTION = 16
		


