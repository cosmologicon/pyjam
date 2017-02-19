import pygame
from . import util, settings, state
from .util import F

screen = None
sx, sy = None, None
x0, y0, Z = None, None, None

def init():
	global screen, sx, sy, x0, y0, Z
	sx, sy = 854, 480
	screen = pygame.display.set_mode((sx, sy))
	util.seth(sy)
	pygame.display.set_caption(settings.gamename)
	
	x0 = 0
	y0 = 0
	Z = 1

def screenpos(pos):
	x, y = pos
	return F([(x - x0) * Z + 427, (y - y0) * Z + 240])

def think(dt):
	global x0, y0
	x0 += state.scrollspeed * dt
	y0 = state.you.y / 2

