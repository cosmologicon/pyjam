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
	rx, ry = pview.centerx0 / scale + d, pview.centery0 / scale + d
	return x0 - rx, y0 - ry, x0 + rx, y0 + ry

def pointvisible(p, d = 1):
	x, y = p
	xmin, ymin, xmax, ymax = vrect(d = d)
	return xmin <= x <= xmax and ymin <= y <= ymax

def linevisible(p0, p1, d = 1):
	(x0, y0), (x1, y1) = p0, p1
	xmin, ymin, xmax, ymax = vrect(d = d)
	if x0 < xmin and x1 < xmin: return False
	if y0 < ymin and y1 < ymin: return False
	if x0 > xmax and x1 > xmax: return False
	if y0 > ymax and y1 > ymax: return False
	return True


