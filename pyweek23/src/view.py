import pygame
from . import util, settings

screen = None

def init():
	global screen
	sx, sy = 854, 480
	screen = pygame.display.set_mode((sx, sy))
	util.seth(sy)
	pygame.display.set_caption(settings.gamename)

