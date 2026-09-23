import math, pygame
from . import pview, graphics
from .pview import T

# B (baseline) coordinates: baseline pixels. +x is right. +y is down. (0, 0) is upper left of screen.
# G (game) coordinates. +x is right. +y is down.
# Angle convention: Like a clock. 0 = up (-y). tau/4 = right (+x).

def angletoward(pos):
	x, y = pos
	if (x, y) == (0, 0): return 0
	return math.atan2(x, -y)
	

def pgangle(A):
	return math.degrees(-A)


class You:
	def __init__(self, pos):
		self.x, self.y = pos
		self.speed = 300
		self.Aface = 0
		self.Amove = None
		self.swing = 0
		self.twalk = 0
		self.walkframes = [0, 1, 2, 1, 0, 3, 4, 3]

	def control(self, dx, dy):
		if dx or dy:
			dx, dy = math.norm((dx, dy))
		self.vx = self.speed * dx
		self.vy = self.speed * dy
		if self.vx or self.vy:
			self.Amove = angletoward((self.vx, self.vy))
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
			

	def draw(self):
		angle = pgangle(self.Aface)
		swing = int(round(self.swing * 2))
		frame = { -2: 4, -1: 3, 0: 0, 1: 1, 2: 2 }[swing]
		graphics.drawimgB(f"walk-{frame}", (self.x, self.y), 0.7, angle)
		graphics.drawcircleB((self.x, self.y), 50, (255, 200, 100))

