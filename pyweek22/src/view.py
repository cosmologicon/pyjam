import pygame, os, os.path, datetime
from . import settings

def init():
	global screen
	pygame.display.set_caption(settings.gamename)
	screen = pygame.display.set_mode(settings.wsize)

def screenshot():
	if not os.path.exists(settings.screenshotpath):
		os.makedirs(settings.screenshotpath)
	timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	filename = os.path.join(settings.screenshotpath, "screenshot-%s.png" % timestamp)
	pygame.image.save(screen, filename)

def clear():
	screen.fill((0, 40, 40))

