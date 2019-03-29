import pygame, math
from . import pview, scene, background

class self:
	pass

def init(up = False, onswap = None):
	self.up = up
	self.onswap = onswap
	self.a = 0
	self.ending = False
	self.done = False
	n = 3 if self.up else 2
	self.dscene = scene.top(n)

def think(dt, controls):
	if self.ending:
		self.a = math.approach(self.a, 0, 2 * dt)
		if self.a == 0 and not self.done:
			self.done = True
			scene.pop()
			if not self.up:
				scene.pop()
	else:
		self.a = math.approach(self.a, 1.2, 4 * dt)
		if self.a == 1.2:
			self.ending = True
			n = 2 if self.up else 3
			self.dscene = scene.top(n)
			if self.onswap is not None:
				self.onswap()
			if self.dscene is not None:
				self.dscene.think(0, controls.clear())

	background.update(dt)

def draw():
	if self.dscene is None:
		background.draw()
	else:
		self.dscene.draw()
	alpha = int(math.clamp(self.a * 255, 0, 255))
	pview.fill((255, 255, 255, alpha))
	



