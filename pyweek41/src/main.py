from . import settings, view, pview, play, control
import pygame

view.init()
play.init()
while control.playing:
	control.think()
	play.think()
	pview.screen.fill((0, 0, 30))
	play.draw()
	pygame.display.flip()

