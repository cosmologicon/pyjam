import pygame, math
from . import pview, scene, background

class self:
	pass

def init(up = False):
	self.up = up
	self.a = 0
	self.ending = False

def think(dt, controls):
	dt *= 6
	if self.ending:
		self.a = math.clamp(self.a - dt, 0, 1)
		if self.a == 0:
			scene.pop()
			if not self.up:
				scene.pop()
	else:
		self.a = math.clamp(self.a + dt, 0, 1.2)
		if self.a == 1.2:
			self.ending = True

	background.update(dt)

def draw():
	n = 2 if self.ending == self.up else 3
	dscene = scene.top(n)
	if dscene is None:
		background.draw()
	else:
		dscene.draw()
	alpha = int(math.clamp(self.a * 255, 0, 255))
	pview.fill((255, 255, 255, alpha))
	



