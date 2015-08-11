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
	return windowpos(X, y, sx, sy, cameraX0, cameray0, cameraR)
def windowpos(X, y, wsx, wsy, X0, y0, scale):
	dX = X - X0
	px = wsx / 2 + math.sin(dX) * y * scale
	py = wsy / 2 + (y0 - math.cos(dX) * y) * scale
	return int(round(px)), int(round(py))
	


# Very rough, a lot of false positives
def onscreen(obj):
	dmax = (sx + sy) / 2 / cameraR
	dy = obj.y - cameray0
	if abs(dy) > dmax:
		return False
	if math.Xmod(obj.X - cameraX0) * cameray0 > dmax:
		return False
	return True

def distance(obj1, obj2):
	dx = math.Xmod(obj1.X - obj2.X) * 2 / (obj1.y + obj2.y)
	dy = obj1.y - obj2.y
	return math.sqrt(dx * dx + dy * dy)

def dbycoord(p1, p2):
	(X1, y1), (X2, y2) = p1, p2
	dx = math.Xmod(X1 - X2) * 2 / (y1 + y2)
	dy = y1 - y2
	return math.sqrt(dx * dx + dy * dy)

def distancefromcamera(X, y):
	d = dbycoord((X, y), (cameraX0, cameray0))
	dscreen = math.sqrt(sx ** 2 + sy ** 2) / 2 / cameraR
	return d / dscreen

