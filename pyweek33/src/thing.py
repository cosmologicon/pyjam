import pygame, math
from . import pview, view, geometry


class You:
	def __init__(self, pos, r = 1, color = None):
		self.x, self.y = pos
		self.r = r
		self.speed = 10
		self.color = color or (100, 50, 50)
	def move(self, dx, dy, room):
		p0 = self.x, self.y
		self.x += dx * self.speed
		self.y += dy * self.speed
		if not room.within(self):
			self.x, self.y = p0
	def reflect(self, mirror):
		pos = geometry.preflect(mirror.p1, mirror.p2, (self.x, self.y))
		return You(pos, self.r, mirror.shade(self.color))
	def draw(self, surf = None):
		pos = view.screenpos((self.x, self.y))
		r = view.screenscale(self.r)
		pygame.draw.circle(surf or pview.screen, self.color, pos, r)


class Room:
	def __init__(self, poly, color = None):
		self.poly = [(a, b) for a, b in poly]
		self.color = color or (40, 40, 50)
	def within(self, obj):
		return geometry.polywithin(self.poly, (obj.x, obj.y), obj.r)
	def reflect(self, mirror):
		poly = geometry.polyreflect(mirror.p1, mirror.p2, self.poly)
		return Room(poly, mirror.shade(self.color))
	def draw(self, surf = None):
		ps = [view.screenpos(p) for p in self.poly]
		pygame.draw.polygon(surf or pview.screen, self.color, ps)


class Mirror:
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2
		self.color = (200, 200, 255)
	def shade(self, color):
		return math.imix(color, self.color, 0.1)
	def draw(self):
		p1 = view.screenpos(self.p1)
		p2 = view.screenpos(self.p2)
		w = view.screenscale(0.2)
		pygame.draw.line(pview.screen, self.color, p1, p2, w)




