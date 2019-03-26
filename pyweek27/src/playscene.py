from __future__ import division
import random, math, pygame
from . import pview, thing, flake, background, ptext
from .pview import T

class self:
	pass

def init():
	self.coins = []
	def randomcircle():
		return (random.uniform(0, 1), random.uniform(0, 1)), random.uniform(0.2, 0.4) ** 2, random.choice(["red", "orange", "yellow", "white", "green"])
	self.design = flake.Design.empty()
	
	self.pointed = None
	self.held = None
	
	self.points = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(20)]
	self.points = [p for p in self.points if math.length(p) < 1]

def think(dt, controls):
	x, y = controls.mpos
	x = (x - 240) / 600
	y = (660 - y) / 600
	self.ppos = x, y
	if controls.mdown:
#		self.design.addcircle((x, y), 0.2, random.choice(["red", "orange", "yellow", "white", "green"]))
		colors = ["#ffffff", "#ddddff", "#ddeeff"]
#		self.design.addshard(self.ppos, (0.06, 0.12), random.choice(colors))
		self.design.addshape("blade", self.ppos, random.choice(colors), width = 0.01)
	background.update(dt)
	x, y = controls.mpos
	x = (x - 880) / 300
	y = (360 - y) / 300
	self.pointcolor = self.design.colorat((x, y))

def draw():
	background.draw()
	self.design.draw((880, 360), 300)
	self.design.drawwedge((240, 660), 600)
	
	for x, y in self.points:
		color = pygame.Color("#7777ff" if self.design.colorat((x, y)) else "#ff7777")
		pygame.draw.circle(pview.screen, pygame.Color("black"), T(880 + 300 * x, 360 - 300 * y), T(8))
		pygame.draw.circle(pview.screen, color, T(880 + 300 * x, 360 - 300 * y), T(6))
	ptext.draw(str(self.pointcolor), bottomright = T(1260, 710), fontsize = T(30))

#	odesign = flake.Design.empty()
#	odesign.addshard(self.ppos, (0.06, 0.12), "#ffffff")
#	odesign.drawoverlay((880, 360), 300)
	

