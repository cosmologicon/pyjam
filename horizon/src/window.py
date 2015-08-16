# We use the polar coordinate system (X, y) that I originally used in Twondy and Zoop.
# X is the angle in radians and y is the distance from the center.
# This approaches a rectangular coordinate system (x, y) in the limit as y goes to infinity,
# with x = Xy. We never use x directly, but for infinitesimal changes, dx = y dX. So for instance,
# objects have x-velocity, and their X coordinate is updates appropriately as dX = v_x dt / y.
# For finite changes, we use the approximation delta-x = y delta-X. This is good for most purposes,
# as long as you don't get too close to the singularity at y = 0.
# X in general is not normalized to the interval [0, tau) or anything like that. When checking
# whether two objects are near each other, we need to always be aware that their X-coordinates may
# be some multiple of tau apart. (Hence the Xmod function.)

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
	global screen, sx, sy, f, camera
	pygame.display.init()
	sx, sy = settings.windowsize
	flags = 0
	if settings.fullscreen:
		modes = list(pygame.display.list_modes())
		if settings.fullscreenmaxwidth:
			modes = [(x, y) for x, y in modes if x <= settings.fullscreenmaxwidth]
		sxmax, symax = max(modes)
		smax = min(sxmax * 9, symax * 16)
		sx, sy = smax // 9, smax // 16
		flags = flags | FULLSCREEN
	f = sy / 480
	screen = pygame.display.set_mode((sx, sy), flags)
	camera = Camera()
	pygame.mouse.set_visible(not settings.fullscreen)


class Camera(object):
	def __init__(self):
		self.X0 = 0
		self.y0 = 100
		self.R = 10
		self.following = None
		self.oldX = None
		self.oldy = None
		self.tfollow = 0
		self.setlimits()
	def setlimits(self):
		buff = 4  # border around the screen
		a = sx / 2 / self.R + buff
		b = sy / 2 / self.R + buff
		ymin = self.y0 - b
		ymax = math.sqrt((self.y0 + b) ** 2 + a ** 2)
		
		self.By0 = ymin
		self.By1 = ymax
		self.BdX = math.atan(a / ymin) if ymin > 1 else math.tau / 2
		self.Cy0 = ymin - settings.regionbuffer
		self.Cy1 = ymax + settings.regionbuffer
		self.CdX = self.BdX + settings.regionbuffer / ymin if self.Cy0 > 1 and ymin > 1 else math.tau
	# within region B
	def on(self, obj):
		return self.By0 <= obj.y <= self.By1 and abs(math.Xmod(self.X0 - obj.X)) <= self.BdX
	# within region C
	def near(self, obj):
		return self.Cy0 <= obj.y <= self.Cy1 and abs(math.Xmod(self.X0 - obj.X)) <= self.CdX
	def think(self, dt):
		self.R = sy / settings.logicalscreensize
		if not self.following:
			return
		if self.tfollow == 0:
			self.X0 = self.following.X
			self.y0 = self.following.y
		else:
			self.tfollow = max(self.tfollow - dt, 0)
			f = (self.tfollow / 0.4) ** 2
			self.X0 = self.following.X * (1 - f) + self.oldX * f
			self.y0 = self.following.y * (1 - f) + self.oldy * f
		self.setlimits()
	def follow(self, obj):
		if obj is self.following:
			return
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
		self.setlimits()

def screenpos(X, y):
	return windowpos(X, y, sx, sy, camera.X0, camera.y0, camera.R)
def windowpos(X, y, wsx, wsy, X0, y0, scale):
	dX = X - X0
	px = wsx / 2 + math.sin(dX) * y * scale
	py = wsy / 2 + (y0 - math.cos(dX) * y) * scale
	return int(round(px)), int(round(py))
	

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

