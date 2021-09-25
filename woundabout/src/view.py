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
	return T(pview.centerx0 + scale * (x - x0), pview.centery0 - scale * (y - y0))

def vrect(d = 1):
	w0, h0 = settings.size0
	rect = pygame.Rect(0, 0, w0 / scale + 2 * d, h0 / scale + 2 * d)
	rect.center = x0, y0
	return rect

def pointvisible(p, d = 1):
	return vrect(d = d).collidepoint(p)

def linevisible(p0, p1, d = 1):
	(x0, y0), (x1, y1) = p0, p1
	rect = pygame.Rect(min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0))
	return vrect(d = d).colliderect(rect)


