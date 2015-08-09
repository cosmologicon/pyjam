from __future__ import division
import pygame
from pygame.locals import *
from src import settings

f = 1.0
def F(x, *args):
	if args:
		return F([x] + list(args))
	if isinstance(x, (int, float)):
		return int(f * x)
	if isinstance(x, (tuple, list)):
		return type(x)(int(f * a for a in x))

def init():
	global screen, sx, sy, f
	sx, sy = settings.windowsize
	sx0, sy0 = settings.windowsize0
	flags = 0
	f = 1.0
	if settings.fullscreen:
		sxmax, symax = max(pygame.display.list_modes())
		f = min(sxmax / sx, symax / sy)
		smax = min(sxmax * sy, symax * sx)
		sx, sy = smax // sy, smax // sx
		flags = flags | FULLSCREEN
	screen = pygame.display.set_mode((sx, sy), flags)

