import pygame
from . import settings, play, view, pview

view.init()
scene = play
scene.init()

clock = pygame.time.Clock()
playing = True
while playing:
	dt = min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_F10:
				pview.cycle_height(settings.heights)
			if event.key == pygame.K_F11:
				pview.toggle_fullscreen()
			if event.key == pygame.K_F12:
				pview.screenshot()

	scene.think(dt)
	scene.draw()
	pygame.display.flip()

