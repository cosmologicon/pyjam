from __future__ import division
import pygame, math, os, datetime
from . import settings, util

screen = None
sx, sy = None, None

def init():
	setwindow()
	pygame.display.set_caption(settings.gamename + (" [DEBUG MODE]" if settings.DEBUG else ""))

def setwindow():
	global screen, sx, sy
	if settings.fullscreen:
		sx, sy = max(pygame.display.list_modes())
		screen = pygame.display.set_mode((sx, sy), pygame.FULLSCREEN)
	else:
		sy = settings.resolution
		sx = int(math.ceil(16 / 9 * sy))
		screen = pygame.display.set_mode((sx, sy))
	util.f = sy / settings.resolution

def screenshot():
	if not os.path.exists("screenshots"):
		os.mkdir("screenshots")
	filename = datetime.datetime.now().strftime("screenshots/screenshot-%Y%m%d%H%M%S.png")
	pygame.image.save(screen, filename)

def togglefullscreen():
	settings.fullscreen = not settings.fullscreen
	setwindow()

