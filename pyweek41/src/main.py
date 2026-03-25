from . import settings, view, pview, play, control
import pygame

view.init()
play.init()
while control.playing:
	control.think()
	play.think()
	play.draw()
	pygame.display.flip()

