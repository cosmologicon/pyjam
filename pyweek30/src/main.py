import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from . import settings, view, ptextgl, control, graphics, pview, world, state, thing, hud, quest

view.init()

pygame.init()
quest.init()
view.init()
control.init()
graphics.init()
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
	if "skip" in kdowns:
		quest.skip()

	if view.incutscene():
		kdowns, kpressed = control.empty()
	if "swap" in kdowns:
		view.swapmode()
	if "act" in kdowns:
		state.act()

	while dtaccum > dt0:
		dtaccum -= dt0
		state.you.control(dt0, kpressed)
		world.think(dt0)
		for island in state.islands:
			island.think(dt0)
		state.you.think(dt0)
		if state.moonrod is not None:
			state.moonrod.think(dt0)
		view.think(dt0)
		hud.think(dt0)
		quest.think(dt0)
		for effect in state.effects:
			effect.think(dt0)
		state.effects[:] = [effect for effect in state.effects if effect.alive]
		kdowns = set()


	view.clear()
	glPushMatrix()
	graphics.draw()
	glDisable(GL_SCISSOR_TEST)
	glPopMatrix()
	hud.draw()
	if False:
		text = "\n".join([
			"%.1ffps" % clock.get_fps(),
			"%.3f, %.3f, %.3f" % tuple(state.you.up),
			"%.2f %.2f" % (state.you.hbob, state.you.h),
		])
		ptextgl.draw(text, (10, 10))
	pygame.display.flip()

pygame.quit()

