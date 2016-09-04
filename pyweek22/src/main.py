from __future__ import division
import pygame
from . import mhack, settings, view

pygame.init()
view.init()

clock = pygame.time.Clock()
playing = True
while playing:
	dt = max(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:	
			if event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_F12:
				view.screenshot()

	view.clear()	
	pygame.display.flip()
pygame.quit()
