import pygame, os.path
from OpenGL.GL import *
from OpenGL.GLU import *
from . import settings
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=2)
from . import view, ptextgl, control, graphics, pview, world, state, thing, hud, quest, sound


view.init()
pygame.mouse.set_visible(False)

pygame.init()
sound.init()
view.init()
graphics.init()
thing.init()
quest.init()
control.init()
hud.init()

if settings.qsavefile and not settings.reset and os.path.exists(settings.qsavefile):
	state.load(settings.qsavefile)


playing = True
clock = pygame.time.Clock()
dt0 = 1 / settings.maxfps
dtaccum = 0
tsave = 0
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	dtaccum += dt
	tsave += dt
	kdowns, kpressed = control.get()
	if "quit" in kdowns:
		playing = False
	if "skip" in kdowns:
		quest.skip()
	if "resolution" in kdowns:
		pview.cycle_height(settings.heights)
	if "fullscreen" in kdowns:
		pview.toggle_fullscreen()

	if view.incutscene():
		kdowns, kpressed = control.empty()
	if "swap" in kdowns and quest.cantab():
		state.ntabs += 1
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
		quest.think(dt0)
		for effect in state.effects:
			effect.think(dt0)
		state.effects[:] = [effect for effect in state.effects if effect.alive]
		state.approachcolor0(quest.color0(), 0.5 * dt0)
		kdowns = set()
	hud.think(dt, kpressed["hint"])
	sound.think(dt)


	view.clear()
	glPushMatrix()
	if quest.ending():
		quest.drawend()
		if quest.done():
			playing = False
	else:
		glPushMatrix()
		glDisable(GL_LIGHTING)
		glDisable(GL_TEXTURE_2D)
		view.perspectivestars()
		view.look()
		glScale(500, 500, 500)
		glCallList(graphics.lists.stars)
		glPopMatrix()
		glClear(GL_DEPTH_BUFFER_BIT)
		view.perspective()
		view.look()
		graphics.draw()
	glPopMatrix()
	hud.draw()
	view.overcut()
	if False:
		text = "\n".join([
			"%.1ffps" % clock.get_fps(),
			"%.3f, %.3f, %.3f" % tuple(state.you.up),
			"%.2f %.2f" % (state.you.hbob, state.you.h),
		])
		ptextgl.draw(text, (10, 10))
	pygame.display.flip()
	
	if settings.qsavefile and tsave >= settings.qsavetime:
		state.save(settings.qsavefile)
		tsave = 0

pygame.quit()

