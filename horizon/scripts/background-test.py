from __future__ import division
import pygame, math, sys
from pygame.locals import *
sys.path.insert(1, sys.path[0] + "/..")
from src import background, window, settings, state

math.tau = 2 * math.pi

window.init()

class camera:
	X0 = 0
	y0 = 100
	R = 2

camera.y0 = state.R
clock = pygame.time.Clock()
playing = True
while playing:
	dt = clock.tick(60) * 0.001
	background.think(dt)
	background.flow(10 * dt)
	for event in pygame.event.get():
		if event.type == KEYDOWN and event.key == K_ESCAPE:
			playing = False
	k = pygame.key.get_pressed()
	camera.X0 += 2 * dt * (k[K_RIGHT] - k[K_LEFT])
	camera.y0 += 100 * dt * (k[K_UP] - k[K_DOWN])

	background.draw(factor = 12, camera = camera)
	pygame.display.flip()

