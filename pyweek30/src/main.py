import pygame
from . import settings, view, ptextgl, control, graphics, pview, world, state, thing

import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


view.init()

pygame.init()
view.init()
control.init()
graphics.init()
state.you = thing.You()

playing = True
clock = pygame.time.Clock()
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	kdowns, kpressed = control.get()
	if "quit" in kdowns:
		playing = False
	if "swap" in kdowns:
		view.swapmode()
	if "act" in kdowns:
		world.act()

	state.you.control(dt, kpressed)

	world.think(dt)
	state.you.think(dt)
	view.think(dt)


	view.clear()
	view.look()
	graphics.draw()
	text = "\n".join([
		"%.1ffps" % clock.get_fps(),
		"%.1f, %.1f, %.1f" % tuple(world.you),
	])
	ptextgl.draw(text, (10, 10))
	pygame.display.flip()

pygame.quit()

