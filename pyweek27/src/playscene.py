from __future__ import division
import random, math, pygame, json, os.path
from . import pview, thing, flake, background, ptext, render, shape, view, hud, settings, client
from . import frostscene, uploadscene, scene
from .pview import T

class self:
	pass

# Zoomed-in wedge on the left
Fspot0 = (280, 710), 700
# Full flake view on the right
Fspot1 = (920, 360), 320

# Region of mouse where the player can interact with the wedge.
Fbox0 = pygame.Rect((220, 0, 460, 720))

def init():
	self.design = flake.Design.empty()
	
#	self.points = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(20)]
#	self.points = [p for p in self.points if math.length(p) < 1]
	
#	self.pshape = shape.Shard((0, 0), "red", (0.06, 0.12))

	self.design.shapes.append(shape.Shard((0, 0.6), "red", (0.06, 0.12)))
	self.design.shapes.append(shape.Shard((0.1, 0.4), "#ffccaa", (0.1, 0.2)))
	self.design.shapes.append(shape.Blade((0.1, 0.7), "#bbbbff", (0.02, 0.06)))
	self.design.shapes.append(shape.Ring((0.1, 0.7), "#ffffbb", 0.04))
	
	self.panchor = None
	self.held = None
	
	self.buttons = [
		hud.Button(((60, 60), 50), "shard", drawtext = False),
		hud.Button(((60, 180), 50), "blade", drawtext = False),
		hud.Button(((pview.w0 - 80, pview.h0 - 200), 50), "upload"),
		hud.Button(((pview.w0 - 80, pview.h0 - 80), 50), "quit"),
	]

def think(dt, controls):
	self.inFbox0 = Fbox0.collidepoint(controls.mpos)
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
	if self.held is None and self.inFbox0:
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
			if self.inFbox0:
				self.design.shapes.append(self.held)
				self.design.undraw()
			self.held = None

	self.jbutton = None
	if not self.held and not self.inFbox0:
		for jbutton, button in enumerate(self.buttons):
			if button.contains(controls.mpos):
				self.jbutton = jbutton

	if self.jbutton is not None and controls.mdown:
		onclick(self.buttons[self.jbutton])

	if pygame.K_F5 in controls.kdowns:
		save()
	if pygame.K_F6 in controls.kdowns:
		client.pullgallery()

def onclick(button):
	if button.text == "quit":
		scene.push(frostscene)
	if button.text == "upload":
		scene.push(uploadscene, self.design, Fspot1)

def draw():
	if pview._fullscreen:
		pygame.mouse.set_visible(True)
	else:
		pygame.mouse.set_visible(not self.inFbox0 or self.held is None)
	background.draw()

	for jbutton, button in enumerate(self.buttons):
		button.draw(lit = (jbutton == self.jbutton))
#	pygame.draw.rect(pview.screen, (0, 0, 0), T(Fbox0))
	self.design.drawwedge(Fspot0)
	self.design.draw(Fspot1)
	render.sector0(Fspot0)
	if self.inFbox0:
		render.sectors(Fspot1)
	
#	for x, y in self.points:
#		p = view.BconvertF(Fspot1, (x, y))
#		color = pygame.Color("#7777ff" if self.design.colorat((x, y)) else "#ff7777")
#		pygame.draw.circle(pview.screen, pygame.Color("black"), T(p), T(8))
#		pygame.draw.circle(pview.screen, color, T(p), T(6))
	ptext.draw(str(self.pointcolor), bottomright = T(1260, 710), fontsize = T(30))

	if self.held and self.inFbox0:
		for j, anchor in enumerate(self.held.anchors):
			color = "white" if j == self.jheld else "orange"
			render.anchor(Fspot0, anchor, color)
		self.held.drawoutline0(Fspot0)
		self.held.drawoutline(Fspot1)
	else:
		for i, j, anchor in self.design.anchors():
			color = "white" if (i, j) == self.panchor else "orange"
			render.anchor(Fspot0, anchor, color)

#	p = view.BconvertF(Fspot0, self.pshape.anchors[0])
#	pygame.draw.circle(pview.screen, pygame.Color("orange"), T(p), T(3))

#	odesign = flake.Design.empty()
#	odesign.addshard(self.ppos, (0.06, 0.12), "#ffffff")
#	odesign.drawoverlay((880, 360), 300)
	
def save():
	state = {
		"design": self.design.getspec(),
	}
	json.dump(state, open(settings.savefilename, "w"))

def canload():
	return os.path.exists(settings.savefilename)

def load():
	state = json.load(open(settings.savefilename, "r"))
	self.design = flake.Design(state["design"])


