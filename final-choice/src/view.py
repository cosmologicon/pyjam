from __future__ import division
import pygame
from pygame.locals import *
from . import util, settings, state, pview
from .pview import T

x0, y0, Z = 0, 0, 1

def init():
	size0 = (480, 854) if settings.portrait else (854, 480)
	h = settings.windowsize
	if settings.portrait: h *= 16 / 9
	pview.set_mode(size0, h, fullscreen = settings.fullscreen, forceres = settings.forceres)
	pygame.display.set_caption(settings.gamename)
	pygame.mouse.set_visible(False)

def screenpos(pos):
	x, y = pos
	dx, dy = (x - x0) * Z, (y - y0) * Z
	if settings.portrait:
		return T([dy + 240, 427 - dx])
	else:
		return T([dx + 427, dy + 240])

def screenpos0(pos):
	x, y = pos
	dx, dy = x * Z, y * Z
	if settings.portrait:
		return T([dy + 240, 427 - dx])
	else:
		return T([dx + 427, dy + 240])

def think(dt):
	global y0
	ymax = state.yrange - state.you.r
	y0max = state.yrange - 240
	a = y0max / (2 * ymax ** 3)
	b = 3 * ymax ** 2 * a
	y0 = b * state.you.y - a * state.you.y ** 3

