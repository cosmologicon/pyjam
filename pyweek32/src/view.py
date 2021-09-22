import pygame, math
from . import pview, settings
from .pview import T


x0, y0 = 0, 0
scale = 40

def init():
	pygame.display.init()
	pygame.display.set_caption(settings.gamename)
	pview.set_mode(settings.size0, settings.height, fullscreen = settings.fullscreen)

def resize(reverse = False):
	pview.cycle_height(settings.heights, reverse = reverse)
	settings.height = pview.height
	settings.save()

def toggle_fullscreen():
	settings.fullscreen = not settings.fullscreen
	settings.save()
	pview.set_mode(fullscreen = settings.fullscreen)
	
def clear():
	pview.fill((10, 20, 30))

def screenpos(worldpos):
	x, y = worldpos
	return T(pview.centerx + scale * (x - x0), pview.centery - scale * (y - y0))


