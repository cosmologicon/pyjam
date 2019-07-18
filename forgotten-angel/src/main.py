from __future__ import division
import pygame
from . import settings, scene, vista, gamescene, buildscene, menuscene

pygame.init()
vista.init()
pygame.display.set_caption(settings.gamename)
scene.push(menuscene)
#scene.push(gamescene)
#scene.push(buildscene)

clock = pygame.time.Clock()
while True:
	scene0 = scene.top()
	if not scene0:
		break
	dt = min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	events = pygame.event.get()
	if settings.DEBUG:
		pygame.display.set_caption("%s | %.1ffps" % (settings.gamename, clock.get_fps()))
	if any(event.type == pygame.QUIT for event in events):
		break

	scene0.think(dt, events, pygame.mouse.get_pos())
	vista.clear()
	scene0.draw()
	vista.flip()
	if any(event.type == pygame.KEYDOWN and event.key == pygame.K_F12 for event in events):
		vista.screenshot()


