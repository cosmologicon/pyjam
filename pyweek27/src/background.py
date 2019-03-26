from __future__ import division
import pygame, math, random
from . import pview

class self:
	size = None

def clear():
	self.size = None

def makesurf():
	self.size = pview.size
	self.w, self.h = self.size
	self.img = pygame.Surface(self.size).convert_alpha()
	self.img.fill((20, 20, 60))

def update(dt):
	if self.size is None:
		makesurf()
	n = 100 * dt
	n = int(n) + (random.random() < n % 1)
	for j in range(n):
		f = random.uniform(0.3, 0.36)
		a = random.uniform(55, 65)
		color = pview.I(f * a, f * a, a)
		width = pview.T(random.uniform(2, 3))
		if random.random() < 1 / 3:
			y = random.random() * self.h
			pygame.draw.line(self.img, color, (0, y), (self.w, y), width)
		else:
			dx = int(self.h / (2 * math.sqrt(3)))
			x = int(random.random() * (self.w + 2 * dx) - dx)
			if random.random() < 1 / 2:
				dx = -dx
			pygame.draw.line(self.img, color, (x - dx, 0), (x + dx, self.h), width)
			

def draw():
	if self.size is None:
		makesurf()
	pview.screen.blit(self.img, (0, 0))


