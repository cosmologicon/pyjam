from __future__ import division
import pygame
from . import mhack, settings, view, state, ptext
from . import scene, playscene, startscene
from .util import F

pygame.init()
view.init()
scene.push(playscene)
#scene.push(startscene)

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
			if event.key == pygame.K_F11:
				view.togglefullscreen()
			if event.key == pygame.K_F12:
				view.screenshot()

	kpressed = pygame.key.get_pressed()
	if kpressed[pygame.K_F1]:
		dt *= 5


	s = scene.top()
	s.think(dt, mpos, mdown, mup)
	s.draw()

	if settings.showfps:
		ptext.draw("%.1ffps" % clock.get_fps(),
			right = F(844), top = F(10), fontsize = F(26), color = "yellow")

	pygame.display.flip()
pygame.quit()
