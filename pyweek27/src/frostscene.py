import pygame, math
from . import pview, scene, background

class self:
	pass

def init(up = False):
	self.up = up
	self.a = 0
	self.ending = False
	self.done = False
	n = 3 if self.up else 2
	self.dscene = scene.top(n)

def think(dt, controls):
	n = 2 if self.ending == self.up else 3
	self.dscene = scene.top(n)

	if self.ending:
		self.a = math.clamp(self.a - dt * 2, 0, 1)
		if self.a == 0 and not self.done:
			self.done = True
			scene.pop()
			if not self.up:
				scene.pop()
	else:
		self.a = math.clamp(self.a + dt * 4, 0, 1.2)
		if self.a == 1.2:
			self.ending = True
			n = 2 if self.up else 3
			dscene = scene.top(n)
			if dscene is not None:
				dscene.think(0, controls.clear())

	background.update(dt)

def draw():
	if self.dscene is None:
		background.draw()
	else:
		self.dscene.draw()
	alpha = int(math.clamp(self.a * 255, 0, 255))
	pview.fill((255, 255, 255, alpha))
	



