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
		
#	self.points = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(20)]
#	self.points = [p for p in self.points if math.length(p) < 1]
	
#	self.pshape = shape.Shard((0, 0), "red", (0.06, 0.12))

	self.design.shapes.append(shape.Shard((0, 0.6), "red", (0.06, 0.12)))
	self.design.shapes.append(shape.Shard((0.1, 0.4), "orange", (0.1, 0.2)))
	
	self.panchor = None
	self.held = None

def think(dt, controls):
	self.ppos = view.FconvertB(Fspot0, controls.mpos)
#	if controls.mdown:
#		self.design.addcircle((x, y), 0.2, random.choice(["red", "orange", "yellow", "white", "green"]))
#		colors = ["#ffffff", "#ddddff", "#ddeeff"]
#		self.design.addshard(self.ppos, (0.06, 0.12), random.choice(colors))
#		self.design.addshape("blade", self.ppos, random.choice(colors), width = 0.01)
	background.update(dt)
	self.pointcolor = self.design.colorat(view.FconvertB(Fspot1, controls.mpos))
#	self.pshape.anchors[0] = self.pshape.constrain(self.ppos, 0)

	self.panchor = None
	if self.held is None:
		panchors = [(math.distance(self.ppos, anchor), i, j) for i, j, anchor in self.design.anchors()]
		if panchors:
			d, i, j = min(panchors)
			if d < 0.03:
				self.panchor = i, j

	if self.panchor and controls.mdown:
		i, self.jheld = self.panchor
		self.held = self.design.shapes.pop(i)
		self.design.undraw()

	if self.held:
		self.held.constrainanchor(self.jheld, self.ppos)
		if controls.mup:
			self.design.shapes.append(self.held)
			self.design.undraw()
			self.held = None

def draw():
	pygame.mouse.set_visible(self.held is None)
	background.draw()
	self.design.drawwedge(Fspot0)
	self.design.draw(Fspot1)
	render.sector0(Fspot0)
	render.sectors(Fspot1)
	
#	for x, y in self.points:
#		p = view.BconvertF(Fspot1, (x, y))
#		color = pygame.Color("#7777ff" if self.design.colorat((x, y)) else "#ff7777")
#		pygame.draw.circle(pview.screen, pygame.Color("black"), T(p), T(8))
#		pygame.draw.circle(pview.screen, color, T(p), T(6))
	ptext.draw(str(self.pointcolor), bottomright = T(1260, 710), fontsize = T(30))

	if self.held:
		for j, anchor in enumerate(self.held.anchors):
			color = "white" if j == self.jheld else "orange"
			render.anchor(Fspot0, anchor, color)
	else:
		for i, j, anchor in self.design.anchors():
			color = "white" if (i, j) == self.panchor else "orange"
			render.anchor(Fspot0, anchor, color)

#	p = view.BconvertF(Fspot0, self.pshape.anchors[0])
#	pygame.draw.circle(pview.screen, pygame.Color("orange"), T(p), T(3))
	if self.held:
		self.held.drawoutline0(Fspot0)
		self.held.drawoutline(Fspot1)

#	odesign = flake.Design.empty()
#	odesign.addshard(self.ppos, (0.06, 0.12), "#ffffff")
#	odesign.drawoverlay((880, 360), 300)
	

