import pygame
from . import pview, view, geometry


class You:
	def __init__(self, pos):
		self.x, self.y = pos
		self.r = 1
		self.speed = 10
	def move(self, dx, dy, room):
		p0 = self.x, self.y
		self.x += dx * self.speed
		self.y += dy * self.speed
		if not room.within(self):
			self.x, self.y = p0
	def draw(self):
		pos = view.screenpos((self.x, self.y))
		r = view.screenscale(self.r)
		pygame.draw.circle(pview.screen, (100, 50, 50), pos, r)


class Room:
	def __init__(self, poly):
		self.poly = [(a, b) for a, b in poly]
	def draw(self):
		color = 40, 40, 50
		ps = [view.screenpos(p) for p in self.poly]
		pygame.draw.polygon(pview.screen, color, ps)
	def within(self, obj):
		return geometry.polywithin(self.poly, (obj.x, obj.y), obj.r)



