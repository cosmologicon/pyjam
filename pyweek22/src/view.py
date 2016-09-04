from __future__ import division
import pygame, os, os.path, datetime
from . import settings, blob
from .util import F

screen = None
blobscreen = None
sx, sy = settings.wsize
x0 = 0
y0 = 0
Z = 2

def init():
	global screen, blobscreen
	pygame.display.set_caption(settings.gamename)
	screen = pygame.display.set_mode((sx, sy))
	blobscreen = pygame.Surface((sx, sy)).convert_alpha()

def screenshot():
	if not os.path.exists(settings.screenshotpath):
		os.makedirs(settings.screenshotpath)
	timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	filename = os.path.join(settings.screenshotpath, "screenshot-%s.png" % timestamp)
	pygame.image.save(screen, filename)

def clear():
	screen.fill((0, 0, 0))
	blobscreen.fill((0, 0, 0, 0))

def applyback():
	screen.blit(blob.tocell(blobscreen), (0, 0))

def screenpos(p):
	x, y = p
	return F([
		sx / 2 + Z * (x - x0),
		sy / 2 + Z * -(y - y0),
	])

def gamepos(p):
	x, y = p
	return (
		x0 + (x - sx / 2) / Z,
		y0 - (y - sy / 2) / Z,
	)

def screenlength(r):
	return F(r * Z)


