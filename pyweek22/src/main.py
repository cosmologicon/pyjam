from __future__ import division
import pygame
from . import mhack, settings, view, state, playscene

pygame.init()
view.init()
playscene.init()

clock = pygame.time.Clock()
playing = True
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	mpos = pygame.mouse.get_pos()
	mdown, mup = False, False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				mdown = True
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:
				mup = True
		if event.type == pygame.KEYDOWN:	
			if event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_F12:
				view.screenshot()
	playscene.think(dt, mpos, mdown, mup)
	playscene.draw()

	pygame.display.flip()
pygame.quit()
