from __future__ import division
import pygame, math
from . import pview, scene, background

class self:
	pass

onswap_ = None

def init(depth0 = 2, depth1 = 2, onswap = None):
	global onswap_
	onswap_ = onswap
	self.a = 0
	self.ending = False
	self.done = False
	self.depth0 = depth0
	self.depth1 = depth1
	self.dscene = scene.top(self.depth0)

def think(dt, controls):
	if self.ending:
		self.a = math.approach(self.a, 0, 2 * dt)
		if self.a == 0 and not self.done:
			self.done = True
			for _ in range(self.depth1 - 1):
				scene.pop()
	else:
		self.a = math.approach(self.a, 1.2, 4 * dt)
		if self.a == 1.2:
			self.ending = True
			self.dscene = scene.top(self.depth1)
			if onswap_ is not None:
				onswap_()
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
	



