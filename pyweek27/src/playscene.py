from __future__ import division
import random, math, pygame
from . import pview, thing, flake, background, ptext, render, shape, view
from .pview import T

class self:
	pass

# Zoomed-in wedge on the left
Fspot0 = (240, 710), 700
# Full flake view on the right
Fspot1 = (880, 360), 320

def init():
	self.coins = []
	def randomcircle():
		return (random.uniform(0, 1), random.uniform(0, 1)), random.uniform(0.2, 0.4) ** 2, random.choice(["red", "orange", "yellow", "white", "green"])
	self.design = flake.Design.empty()
	
	self.pointed = None
	self.held = None
	
	self.points = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(20)]
	self.points = [p for p in self.points if math.length(p) < 1]
	
	self.pshape = shape.Shard((0, 0), "red", (0.06, 0.12))

def think(dt, controls):
	self.ppos = view.FconvertB(Fspot0, controls.mpos)
	if controls.mdown:
#		self.design.addcircle((x, y), 0.2, random.choice(["red", "orange", "yellow", "white", "green"]))
		colors = ["#ffffff", "#ddddff", "#ddeeff"]
		self.design.addshard(self.ppos, (0.06, 0.12), random.choice(colors))
#		self.design.addshape("blade", self.ppos, random.choice(colors), width = 0.01)
	background.update(dt)
	self.pointcolor = self.design.colorat(view.FconvertB(Fspot1, controls.mpos))
	self.pshape.anchors[0] = self.pshape.constrain(self.ppos, 0)

def draw():
	background.draw()
	self.design.drawwedge(Fspot0)
	self.design.draw(Fspot1)
	render.sector0(Fspot0)
	render.sectors(Fspot1)
	
	for x, y in self.points:
		color = pygame.Color("#7777ff" if self.design.colorat((x, y)) else "#ff7777")
		pygame.draw.circle(pview.screen, pygame.Color("black"), T(880 + 300 * x, 360 - 300 * y), T(8))
		pygame.draw.circle(pview.screen, color, T(880 + 300 * x, 360 - 300 * y), T(6))
	ptext.draw(str(self.pointcolor), bottomright = T(1260, 710), fontsize = T(30))

	p = view.BconvertF(Fspot0, self.pshape.anchors[0])
	pygame.draw.circle(pview.screen, pygame.Color("orange"), T(p), T(3))
	self.pshape.drawoutline0(Fspot0)
	self.pshape.drawoutline(Fspot1)

#	odesign = flake.Design.empty()
#	odesign.addshard(self.ppos, (0.06, 0.12), "#ffffff")
#	odesign.drawoverlay((880, 360), 300)
	

