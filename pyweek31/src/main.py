import os.path
import pygame
from . import pview, ptext
from . import settings, state, view, hud, controls, progress, sound
from . import scene, playscene, menuscene
from .pview import T

ptext.DEFAULT_FONT_NAME = "MiltonianTattoo"
ptext.FONT_NAME_TEMPLATE = os.path.join("fonts", "%s.ttf")

pygame.init()
view.init()
pygame.mixer.init()
if settings.reset:
	progress.reset()
	state.reset()
progress.load()
state.load()
if settings.unlockall:
	progress.unlockall()
	progress.save()
scene.push(menuscene)
if os.path.exists(settings.qsavename):
	scene.push(playscene)
	playscene.init()
sound.playmusic(settings.mtrack)

playing = True
clock = pygame.time.Clock()
dtaccum = 0
tsave = 0
while playing:
	currentscene = scene.current()
	if currentscene is None:
		break

	cstate = controls.ControlState()
	currentscene.control(cstate)

	if "quit" in cstate.events or "quit" in cstate.kdowns:
		playing = False
	if "screenshot" in cstate.kdowns:
		pview.screenshot()
	if "resize" in cstate.kdowns:
		view.resize()
	if "fullscreen" in cstate.kdowns:
		view.toggle_fullscreen()

	if settings.DEBUG and cstate.kpressed[pygame.K_F2]:
		state.shuffle()
	if settings.DEBUG and cstate.kpressed[pygame.K_F3]:
		print(state.getspec())

	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	dtaccum += dt
	dt0 = 1 / settings.maxfps
	while dtaccum >= dt0:
		currentscene.think(dt0)
		dtaccum -= dt0

	view.clear()
	currentscene.draw()

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

	tsave += dt
	if settings.tautosave is not None and tsave >= settings.tautosave:
		tsave = 0
		state.save()
state.save()
progress.save()
settings.save()

