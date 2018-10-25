from __future__ import division
import pygame
from pygame.locals import *
from . import maff, settings, view, scene, gamescene, graphics, ptext, sound

view.init()
graphics.init()
pygame.mixer.init()
scene.push(gamescene)

playing = True
clock = pygame.time.Clock()
dt0 = 1 / settings.maxfps
dt = 0
while playing:
	dt += min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	kdowns = set()
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			kdowns.add(event.key)
		if event.type == QUIT:
			playing = False
	kpressed = pygame.key.get_pressed()
	pressed = { key: any(kpressed[code] for code in codes) for key, codes in settings.keymap.items() }
	downs = { key: any(code in kdowns for code in codes) for key, codes in settings.keymap.items() }
	if downs["quit"]:
		playing = False
	s = scene.top()
	if s is None:
		break
	while dt > dt0:
		dt -= dt0
		s.think(dt0, pressed, downs)
		downs = { key: False for key in downs }
	s.draw()
	if settings.DEBUG:
		text = "%s: %.1ffps" % (settings.gamename, clock.get_fps())
		pygame.display.set_caption(text)
		text = "%.1ffps" % clock.get_fps()
		ptext.draw(text, bottomleft = (10, 10), fontsize = 22)
	pygame.display.flip()
	if K_F12 in kdowns:
		view.screenshot()
pygame.quit()
