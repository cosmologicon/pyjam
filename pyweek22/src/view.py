from __future__ import division
import pygame, os, os.path, datetime
from . import settings
from .util import F

screen = None
sx, sy = settings.wsize
x0 = 0
y0 = 0
Z = 3

def init():
	global screen
	pygame.display.set_caption(settings.gamename)
	screen = pygame.display.set_mode((sx, sy))

def screenshot():
	if not os.path.exists(settings.screenshotpath):
		os.makedirs(settings.screenshotpath)
	timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	filename = os.path.join(settings.screenshotpath, "screenshot-%s.png" % timestamp)
	pygame.image.save(screen, filename)

def clear():
	screen.fill((0, 40, 40))

def screenpos((x, y)):
	return F([
		sx / 2 + Z * (x - x0),
		sy / 2 + Z * -(y - y0),
	])

def screenlength(r):
	return F(r * Z)


