from __future__ import division
import pygame
from pygame.locals import *
from . import maff, settings, view, scene, gamescene, graphics, ptext, sound, state, mapscene, loadscene, pview
from .pview import T

ptext.FONT_NAME_TEMPLATE = "data/fonts/%s.ttf"
view.init()
pygame.display.set_caption(settings.gamename)
pygame.mixer.init()
graphics.init()
scene.push(loadscene)
#scene.push(mapscene)

playing = True
clock = pygame.time.Clock()
dt0 = 1 / settings.maxfps
dt = 0
pygame.mouse.get_rel()
while playing:
	dt += min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	kdowns = set()
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			kdowns.add(event.key)
		if event.type == QUIT:
			playing = False
		if event.type == MOUSEBUTTONDOWN and event.button == 1:
			settings.manualcamera = not settings.manualcamera
			view.grabmouse(True)
	dmx, dmy = pygame.mouse.get_rel()
	dmx /= pview.w
	dmy /= pview.w
	kpressed = pygame.key.get_pressed()
	pressed = { key: any(kpressed[code] for code in codes) for key, codes in settings.keymap.items() }
	downs = { key: any(code in kdowns for code in codes) for key, codes in settings.keymap.items() }
	if downs["quit"]:
		playing = False
	# CHEAT CODES
	if K_1 in kdowns:
		state.teleport("NW")
	if K_2 in kdowns:
		state.teleport("NE")
	if K_3 in kdowns:
		state.teleport("SW")
	if K_4 in kdowns:
		state.teleport("SE")
	if K_0 in kdowns:
		state.teleport("home")
	if K_5 in kdowns:
		state.food = state.foodmax
	if settings.DEBUG and pressed["debugspeed"]:
		dt *= 10
		state.food = 1000
	s = scene.top()
	if s is None:
		break
	while dt > dt0:
		dt -= dt0
		s.think(dt0, pressed, downs, dmx, dmy)
		downs = { key: False for key in downs }
	s.draw()
	if settings.DEBUG:
		text = "%s: %.1ffps" % (settings.gamename, clock.get_fps())
		pygame.display.set_caption(text)
		text = "%.1ffps" % clock.get_fps()
		ptext.draw(text, bottomleft = T(10, 10), fontsize = T(22))
	pygame.display.flip()
	if loadscene.self.done:
		if K_F10 in kdowns:
			view.cycle_height()
		if K_F11 in kdowns:
			view.toggle_fullscreen()
		if K_F12 in kdowns:
			view.screenshot()
graphics.cleanup()
state.clean()
pygame.quit()
