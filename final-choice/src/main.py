from __future__ import division
import pygame, os, datetime
from pygame.locals import *
from . import settings, view, ptext, background, state, sound, pview
from . import scene, playscene, losescene, climaxscene, creditsscene, winscene
from .pview import T

if settings.vidcap:
	from . import vidcap


pygame.init()
view.init()
background.init()
sound.init()

ptext.FONT_NAME_TEMPLATE = os.path.join("data", "font", "%s.ttf")

state.startup()
#scene.push(playscene, 1)
#scene.push(climaxscene)
#state.met = set("12347XJG")
#state.saved = set("1234JG")
#scene.push(winscene)
#scene.push(creditsscene)

clock = pygame.time.Clock()
dtexcess = 0
while scene.stack:
	dt = min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	sound.think(dt)
	top = scene.stack[-1]
	kdowns = set()
	for event in pygame.event.get():
		if event.type == QUIT:
			scene.quit()
		if event.type == KEYDOWN:
			kdowns.add(event.key)
	kpressed = pygame.key.get_pressed()
	if settings.DEBUG and kpressed[K_F7]:
		dt *= 20

	dtexcess += dt
	kd = kdowns
	while dtexcess >= 1 / settings.maxfps:
		top.think(1 / settings.maxfps, kd, kpressed)
		dtexcess -= 1 / settings.maxfps
		kd = set()
	top.draw()
	if settings.DEBUG:
		text = "\n".join([
			"F2: toggle DEBUG mode",
			"F10: toggle portrait mode",
			"F11: toggle fullscreen",
			"F12: screenshot",
			"objsize: %d %d %d" % (len(state.goodbullets), len(state.badbullets), len(state.enemies)),
			"met: " + "".join(sorted(state.met)),
			"saved: " + "".join(sorted(state.saved)),
			"%.1ffps" % clock.get_fps(),
		])
		h = 849 if settings.portrait else 475
		ptext.draw(text, bottomleft = T(5, h), fontsize = T(18), color = "white")
	pygame.display.flip()

	if settings.isdown("quit", kdowns):
		scene.quit()
	if settings.isdown("fullscreen", kdowns):
		settings.fullscreen = not settings.fullscreen
		view.init()
	if settings.isdown("portrait", kdowns):
		settings.portrait = not settings.portrait
		view.init()
	if settings.isdown("screenshot", kdowns):
		pview.screenshot()
	if settings.DEBUG and settings.isdown("quicksave", kdowns):
		state.save(settings.quicksavefile)
	if settings.DEBUG and settings.isdown("quickload", kdowns):
		state.load(settings.quicksavefile)
	if settings.isdown("toggledebug", kdowns):
		settings.DEBUG = not settings.DEBUG
	if settings.DEBUG and K_1 in kdowns:
		state.gotostage(1)
	if settings.DEBUG and K_2 in kdowns:
		state.gotostage(2)
	if settings.DEBUG and K_3 in kdowns:
		state.gotostage(3)
	if settings.DEBUG and K_4 in kdowns:
		state.gotostage(4)
	if settings.DEBUG and K_F8 in kdowns:
		del state.bosses[:], state.waves[:], state.spawners[:]
	#pygame.display.set_caption("%s - %.1ffps" % (settings.gamename, clock.get_fps()))

pygame.quit()



