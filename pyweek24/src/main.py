from __future__ import division, print_function
import pygame
from . import settings, view, pview, ptext, playscene
from .pview import T

view.init()
playscene.init()

clock = pygame.time.Clock()
playing = True
while playing:
	dt = 0.001 * clock.tick(settings.maxfps)
	dt = min(dt, 1 / settings.minfps)

	kdowns = []
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			kdowns.append(event.key)
		if event.type == pygame.QUIT:
			playing = False
	
	kpressed = pygame.key.get_pressed()

	playscene.think(dt, kdowns, kpressed)

	if pygame.K_F11 in kdowns:
		pview.toggle_fullscreen()
	playscene.draw()
	if settings.DEBUG:
		ptext.draw("%.1ffps" % clock.get_fps(), bottomleft = T(10, 470), fontsize = T(16))

	if pygame.K_F12 in kdowns:
		pview.screenshot()

	pygame.display.flip()
	if pygame.K_ESCAPE in kdowns:
		playing = False

