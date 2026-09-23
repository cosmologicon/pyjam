# Unless otherwise noted, all positions and distances in this module are game (G) coodinates.

import math, pygame
from . import pview, graphics, view, settings, geometry
from .pview import T

class You:
	imgscale = 0.025
	def __init__(self, pos):
		self.r = 1
		self.x, self.y = pos
		self.speed = 10
		self.Aface = 0
		self.Amove = None
		self.swing = 0
		self.twalk = 0

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
		self.x += self.vx * dt
		self.y += self.vy * dt
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
		posB = view.BconvertG((self.x, self.y))
		angle = geometry.pgangle(self.Aface)
		scaleB = view.BscaleG(self.imgscale * self.r)
		graphics.drawimgB(self.currentimg(), posB, scaleB, angle)
		if settings.DEBUG:
			graphics.drawcircleB(posB, view.BscaleG(self.r), (255, 200, 100))

