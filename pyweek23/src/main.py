from __future__ import division
import pygame
from pygame.locals import *
from . import settings, view, ptext
from . import scene, playscene
from .util import F

pygame.init()
view.init()

scene.add(playscene)

clock = pygame.time.Clock()
while scene.stack:
	dt = min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	top = scene.stack[-1]
	kdowns = set()
	for event in pygame.event.get():
		if event.type == QUIT:
			scene.quit()
		if event.type == KEYDOWN:
			kdowns.add(event.key)
	if K_ESCAPE in kdowns:
		scene.quit()
	kpressed = pygame.key.get_pressed()

	top.think(dt, kdowns, kpressed)
	top.draw()
	if settings.DEBUG:
		text = "%.1ffps" % clock.get_fps()
		ptext.draw(text, bottomleft = F(5, 475), fontsize = F(18), color = "white", owidth = 1)
	pygame.display.flip()

pygame.quit()



