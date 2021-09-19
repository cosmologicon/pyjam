import pygame
from . import pview, settings

def init():
	pygame.display.init()
	pygame.display.set_caption(settings.gamename)
	pview.set_mode(settings.size0, settings.height, fullscreen = settings.fullscreen)

def resize(reverse = False):
	pview.cycle_height(settings.heights, reverse = reverse)
	settings.height = pview.height
	settings.save()

def togglefullscreen():
	settings.fullscreen = not settings.fullscreen
	settings.save()
	pview.set_mode(fullscreen = settings.fullscreen)
	
def clear():
	pview.fill((10, 20, 30))


