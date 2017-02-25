from __future__ import division
import pygame
from pygame.locals import *
from . import util, settings, state
from .util import F

screen = None
sx, sy = None, None
x0, y0, Z = 0, 0, 1

def init():
	global screen, sx, sy
	aspect = 9 / 16 if settings.portrait else 16 / 9
	if settings.fullscreen and not settings.forceres:
		sx0, sy0 = max(pygame.display.list_modes())
		sx, sy = min((sx0, int(round(sx0 / aspect))), (int(round(sy0 * aspect)), sy0))
	else:
		sy = settings.windowsize
		sx = int(round(sy * 16 / 9))
		if sy == 480: sx = 854  # special case to match YouTube video size
		if settings.portrait:
			sx, sy = sy, sx
	flags = 0
	if settings.fullscreen: flags |= FULLSCREEN
	screen = pygame.display.set_mode((sx, sy), flags)
	util.seth(sx if settings.portrait else sy)
	pygame.display.set_caption(settings.gamename)
	pygame.mouse.set_visible(False)


def screenpos(pos):
	x, y = pos
	dx, dy = (x - x0) * Z, (y - y0) * Z
	if settings.portrait:
		return F([dy + 240, 427 - dx])
	else:
		return F([dx + 427, dy + 240])

def screenpos0(pos):
	x, y = pos
	dx, dy = x * Z, y * Z
	if settings.portrait:
		return F([dy + 240, 427 - dx])
	else:
		return F([dx + 427, dy + 240])

def think(dt):
	global y0
	y0 = state.you.y / 2

