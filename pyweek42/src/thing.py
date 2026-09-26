# Unless otherwise noted, all positions and distances in this module are game (G) coodinates.

import math, pygame
from . import pview, graphics, view, settings, geometry
from .pview import T

class You:
	imgscale = 0.025
	def __init__(self, pos):
		self.r = 1
		self.pos = pos
		self.speed = 10
		self.Aface = 0
		self.Amove = None
		self.swing = 0
		self.twalk = 0

	def scoot(self, dpos):
		self.pos = geometry.vecadd(self.pos, dpos)

	def control(self, dx, dy):
		if dx or dy:
			dx, dy = math.norm((dx, dy))
		self.vx = self.speed * dx
		self.vy = self.speed * dy
		if self.vx or self.vy:
			self.Amove = geometry.angletoward((self.vx, self.vy))
		else:
			self.Amove = None

	def think(self, dt):
		self.scoot((self.vx * dt, self.vy * dt))
		if self.Amove is not None:
			self.Aface = math.approachA(self.Aface, self.Amove, 10 * dt)
			self.twalk += dt
			self.swing = math.sin(10 * self.twalk)
		else:
			self.twalk = 0
			self.swing = math.approach(self.swing, 0, 5 * dt)

	def currentimg(self):			
		jswing = int(round(self.swing * 2))
		frame = { -2: 4, -1: 3, 0: 0, 1: 1, 2: 2 }[jswing]
		return f"walk-{frame}"

	def draw(self):
		angle = geometry.pgangle(self.Aface)
		scale = self.imgscale * self.r
		graphics.drawimgG(self.currentimg(), self.pos, scale, angle)
		if settings.DEBUG:
			graphics.drawcircleG(self.pos, self.r, (255, 200, 100))


class CircleHazard:
	def __init__(self, pos, r):
		self.pos = pos
		self.r = r

	def hitsyou(self, you):
		return math.distance(self.pos, you.pos) < self.r + you.r

	def draw(self):
		graphics.drawcircleG(self.pos, self.r, (255, 0, 0))

