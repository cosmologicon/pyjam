# We use the polar coordinate system (X, y) that I originally used in Twondy and Zoop.
# X is the angle in radians and y is the distance from the center.
# This approaches a rectangular coordinate system (x, y) in the limit as y goes to infinity,
# with x = Xy. We never use x directly, but for infinitesimal changes, dx = y dX. So for instance,
# objects have x-velocity, and their X coordinate is updates appropriately as dX = v_x dt / y.
# For finite changes, we use the approximation delta-x = y delta-X. This is good for most purposes,
# as long as you don't get too close to the singularity at y = 0.

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


class Camera(object):
	def __init__(self):
		self.X0 = 0
		self.y0 = 100
		self.R = 10
		self.following = None
		self.oldX = None
		self.oldy = None
		self.tfollow = 0
	def think(self, dt):
		self.R = sy / 54
		if not self.following:
			return
		if self.tfollow == 0:
			self.X0 = self.following.X
			self.y0 = self.following.y
		else:
			self.tfollow = max(self.tfollow - dt, 0)
			f = self.tfollow / 0.4
			self.X0 = self.following.X * (1 - f) + self.oldX * f
			self.y0 = self.following.y * (1 - f) + self.oldy * f
	def follow(self, obj):
		oldfollow = self.following
		self.following = obj
		self.tfollow = 0.4
		self.oldX = obj.X + math.Xmod(self.X0 - obj.X)
		self.oldy = self.y0
		if oldfollow is None:
			self.tfollow = 0
			self.think(0)
	def dump(self):
		return [self.X0, self.y0, self.R, (self.following.thingid if self.following else None),
			self.oldX, self.oldy, self.tfollow]
	def load(self, obj):
		from src import thing
		(self.X0, self.y0, self.R, self.following, self.oldX, self.oldy, self.tfollow) = obj
		if self.following is not None:
			self.following = thing.get(self.following)

camera = Camera()

def screenpos(X, y):
	return windowpos(X, y, sx, sy, camera.X0, camera.y0, camera.R)
def windowpos(X, y, wsx, wsy, X0, y0, scale):
	dX = X - X0
	px = wsx / 2 + math.sin(dX) * y * scale
	py = wsy / 2 + (y0 - math.cos(dX) * y) * scale
	return int(round(px)), int(round(py))
	


# Very rough, a lot of false positives
def onscreen(obj):
	dmax = (sx + sy) / 2 / camera.R
	dy = obj.y - camera.y0
	if abs(dy) > dmax:
		return False
	if abs(math.Xmod(obj.X - camera.X0)) * camera.y0 > dmax:
		return False
	return True

def nearscreen(obj):
	dmax = (sx + sy) / 2 / camera.R * 3
	dy = obj.y - camera.y0
	if abs(dy) > dmax:
		return False
	if abs(math.Xmod(obj.X - camera.X0)) * camera.y0 > dmax:
		return False
	return True

def distance(obj1, obj2):
	dx = math.Xmod(obj1.X - obj2.X) * (obj1.y + obj2.y) / 2
	dy = obj1.y - obj2.y
	return math.sqrt(dx ** 2 + dy ** 2)

def dbycoord(p1, p2):
	(X1, y1), (X2, y2) = p1, p2
	dx = math.Xmod(X1 - X2) * 2 / (y1 + y2)
	dy = y1 - y2
	return math.sqrt(dx * dx + dy * dy)

def distancefromcamera(X, y):
	d = dbycoord((X, y), (camera.X0, camera.y0))
	dscreen = math.sqrt(sx ** 2 + sy ** 2) / 2 / camera.R
	return d / dscreen

