import pygame
from pygame.locals import *
from src import settings

screen = None
sx, sy = settings.windowsize
sf = 1.0

def init():
	global screen, sx, sy, sf
	pygame.display.init()
	sx, sy = settings.windowsize
	sf = 1.0
	if settings.fullscreen:
		sxmax, symax = max(pygame.display.list_modes())
		s = min(sxmax * sy, symax * sx)
		sx, sy = int(s / sy), int(s / sx)
		sf = 1.0 * sx / settings.windowsize[0]
	flags = FULLSCREEN if settings.fullscreen else 0
	screen = pygame.display.set_mode((sx, sy), flags)
	pygame.display.set_caption(settings.gamename)

def F(x):
	if isinstance(x, (int, float)):
		return int(sf * x)
	if isinstance(x, (pygame.Rect, list, tuple)):
		return type(x)([int(sf * a) for a in x])

