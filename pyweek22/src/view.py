from __future__ import division
import pygame, os, os.path, datetime
from . import settings, blob, util
from .util import F

screen = None
blobscreen = None
x0 = 0
y0 = 0
Z = 2

def init():
	global screen, blobscreen, sx, sy
	pygame.display.set_caption(settings.gamename)
	sx, sy = settings.wsize
	flags = 0
	if settings.fullscreen:
		sx0, sy0 = max(pygame.display.list_modes())
		if sx0 * sy > sy0 * sx:
			sx, sy = int(round(sy0 * sx / sy)), sy0
		else:
			sx, sy = sx0, int(round(sx0 * sy / sx))
		flags = flags or pygame.FULLSCREEN
	util.f = sy / 480
	screen = pygame.display.set_mode((sx, sy), flags)
	blobscreen = pygame.Surface((sx, sy)).convert_alpha()

def togglefullscreen():
	settings.fullscreen = not settings.fullscreen
	init()

def screenshot():
	if not os.path.exists(settings.screenshotpath):
		os.makedirs(settings.screenshotpath)
	timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	filename = os.path.join(settings.screenshotpath, "screenshot-%s.png" % timestamp)
	pygame.image.save(screen, filename)

def clear():
	screen.fill((0, 0, 0))
	blobscreen.fill((0, 0, 0, 0))

def drawoverlay(alpha = 0.8, color = (0, 0, 0)):
	overlay = pygame.Surface(screen.get_size()).convert_alpha()
	overlay.fill((color[0], color[1], color[2], int(alpha * 255)))
	screen.blit(overlay, (0, 0))

def applyback():
	screen.blit(blob.tocell(blobscreen), (0, 0))

def screenpos(p):
	x, y = p
	return F([
		854 / 2 + Z * (x - x0),
		480 / 2 + Z * -(y - y0),
	])

def gamepos(p):
	x, y = p
	return (
		x0 + (x - sx / 2) / Z / util.f,
		y0 - (y - sy / 2) / Z / util.f,
	)

def screenlength(r):
	return F(r * Z)


