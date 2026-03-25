from . import settings, view, pview, play, control
import pygame

view.init()
play.init()
clock = pygame.time.Clock()
while control.playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	play.think(dt)
	play.draw()
	pygame.display.flip()

