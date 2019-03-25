from __future__ import division
import random
from . import pview, thing, flake, background

class self:
	pass

def init():
	self.coins = []
	def randomcircle():
		return (random.uniform(0, 1), random.uniform(0, 1)), random.uniform(0.2, 0.4) ** 2, random.choice(["red", "orange", "yellow", "white", "green"])
	self.design = flake.Design.empty()
	
	self.pointed = None
	self.held = None

def think(dt, controls):
	if controls.mdown:
		x, y = controls.mpos
		x = (x - 240) / 600
		y = (660 - y) / 600
		self.design.addcircle((x, y), 0.2, random.choice(["red", "orange", "yellow", "white", "green"]))
	background.update(dt)

def draw():
	background.draw()
	self.design.draw((880, 360), 300)
	self.design.drawwedge((240, 660), 600)


