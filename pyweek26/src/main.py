import pygame
from pygame.locals import *
from . import settings, view, scene, gamescene

view.init()
scene.push(gamescene)

playing = True
clock = pygame.time.Clock()
while playing:
	dt = clock.tick(settings.maxfps) * 0.001
	kdowns = set()
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			kdowns.add(event.key)
		if event.type == QUIT:
			playing = False
	if K_ESCAPE in kdowns:
		playing = False
	kpressed = pygame.key.get_pressed()
	s = scene.top()
	if s is None:
		break
	s.think(dt, kpressed, kdowns)
	s.draw()
	if settings.DEBUG:
		text = "%s: %.1ffps" % (settings.gamename, clock.get_fps())
		pygame.display.set_caption(text)
	pygame.display.flip()
pygame.quit()
