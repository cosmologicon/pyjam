from __future__ import division
import pygame, math
from pygame.locals import *
from src import settings

f = 1.0
def F(x, *args):
	if args:
		return F([x] + list(args))
	if isinstance(x, (int, float)):
		return int(f * x)
	if isinstance(x, (tuple, list)):
		return type(x)(int(f * a) for a in x)

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

cameraX0 = 0
cameray0 = 100
cameraR = 10
def screenpos(X, y):
	dX = X - cameraX0
	px = sx / 2 + math.sin(dX) * y * cameraR
	py = sy / 2 + (cameray0 - math.cos(dX) * y) * cameraR
	return int(round(px)), int(round(py))

def distance(obj1, obj2):
	dx = math.Xmod(obj1.X - obj2.X) * 2 / (obj1.y + obj2.y)
	dy = obj1.y - obj2.y
	return math.sqrt(dx * dx + dy * dy)

