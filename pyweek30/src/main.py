import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from . import settings, view, ptextgl, control, graphics, pview, world, state, thing, hud

view.init()

pygame.init()
view.init()
control.init()
graphics.init()
state.you = thing.You()
state.tide = 0
thing.init()
hud.init()

playing = True
clock = pygame.time.Clock()
dt0 = 1 / settings.maxfps
dtaccum = 0
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	dtaccum += dt
	kdowns, kpressed = control.get()
	if "quit" in kdowns:
		playing = False
	if "swap" in kdowns:
		view.swapmode()
	if "act" in kdowns:
		world.act()

	while dtaccum > dt0:
		dtaccum -= dt0
		state.you.control(dt0, kpressed)
		world.think(dt0)
		state.you.think(dt0)
		state.moonrod.think(dt0)
		view.think(dt0)
		hud.think(dt0)
		kdowns = set()


	view.clear()
	glPushMatrix()
	view.look()
	graphics.draw()
	glPopMatrix()
	hud.draw()
	text = "\n".join([
		"%.1ffps" % clock.get_fps(),
		"%.3f, %.3f, %.3f" % tuple(state.you.up),
		"%.2f %.2f" % (state.you.hbob, state.you.h),
		"%.2f" % (state.islands[-1].distout(state.you.up)),
	])
	ptextgl.draw(text, (10, 10))
	pygame.display.flip()

pygame.quit()

