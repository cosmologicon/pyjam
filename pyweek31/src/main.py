import pygame
from . import pview, ptext
from . import settings, state, view, hud, controls
from . import playscene
from .pview import T

view.init()
playscene.init()
state.load()

playing = True
clock = pygame.time.Clock()
dtaccum = 0
tsave = 0
while playing:
	cstate = controls.ControlState()

	if "quit" in cstate.events or "quit" in cstate.kdowns:
		playing = False
	if "screenshot" in cstate.kdowns:
		pview.screenshot()
	if "resize" in cstate.kdowns:
		view.resize()
	if "fullscreen" in cstate.kdowns:
		view.toggle_fullscreen()
	if cstate.scroll:
		view.zoom(cstate.scroll, cstate.mposV)

	playscene.control(cstate)
	if settings.DEBUG and cstate.kpressed[pygame.K_F2]:
		state.shuffle()
	if settings.DEBUG and cstate.kpressed[pygame.K_F3]:
		print(state.getspec())

	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	tsave += dt
	if settings.DEBUG and cstate.kpressed[pygame.K_F1]:
		dt *= 5
	dtaccum += dt

	dt0 = 1 / settings.maxfps
	while dtaccum >= dt0:
		playscene.think(dt0)
		dtaccum -= dt0

	view.clear()
	playscene.draw()

	if settings.DEBUG:
		xG, yG = view.GconvertV(cstate.mposV)
		xH, yH = view.HnearesthexH(view.HconvertV(cstate.mposV))
		text = "\n".join([
			"selected: %s" % hud.selected(),
			"%.1ffps" % clock.get_fps(),
			"[ %.2f, %.2f ]  [ %d, %d ]" % (xG, yG, xH, yH),
		])
		ptext.draw(text, bottomleft = T(5, pview.h0 - 5))

	pygame.display.flip()
	if settings.tautosave is not None and tsave >= settings.tautosave:
		tsave = 0
		state.save()
state.save()

