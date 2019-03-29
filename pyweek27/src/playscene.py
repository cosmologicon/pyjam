from __future__ import division
import random, math, pygame, json, os.path
from . import pview, thing, flake, background, ptext, render, shape, view, hud, settings, client
from . import frostscene, uploadscene, winscene, scene, progress, stagedata
from .pview import T

class self:
	pass

# Zoomed-in wedge on the left
Fspot0 = (280, 710), 700
# Full flake view on the right
Fspot1 = (920, 360), 320

# Region of mouse where the player can interact with the wedge.
Fbox0 = pygame.Rect((220, 0, 460, 720))

def init(stage):
	self.stage = stage
	self.design = flake.Design.empty()
	
#	self.points = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(20)]
#	self.points = [p for p in self.points if math.length(p) < 1]
	
#	self.pshape = shape.Shard((0, 0), "red", (0.06, 0.12))

	self.panchor = None
	self.held = None
	
	self.store = []
	
	if stage == "free":
		if "Shard" in progress.shapes:
			self.store.append([shape.Shard((0, 0), "white", (0.06, 0.12)), None])
		if "Blade" in progress.shapes:
			self.store.append([shape.Blade((0, 0), "white", (0.02, 0.06)), None])
	if stage in stagedata.store:
		for k, v in stagedata.store[stage]:
			if k == "Shard":
				self.store.append([shape.Shard((0, 0), "white", (0.06, 0.12)), v])
				


	self.buttons = [
		hud.Button(((1200, 640), 50), "Quit"),
	]
	if self.stage == "free":
		self.buttons.append(hud.Button(((640, 640), 50), "Share"))

	self.yespoints = []
	self.nopoints = []
	if stage in stagedata.points:
		yes, no = stagedata.points[stage]
		for a, r, n in yes:
			if n % 2 == 1:
				a = 1 - a
			C, S = math.CS((n + a) / 12 * math.tau, r)
			self.yespoints.append((S, C))
	self.yescovers = [False for _ in self.yespoints]
	self.nocovers = [False for _ in self.nopoints]
	self.todo = bool(self.yescovers or self.ycovers)
	self.done = False
	self.pushed = False
	self.tdone = 0


	for j, _ in enumerate(self.store):
		self.buttons.append(hud.Button(((60, 60 + 120 * j), 50), "store-%d" % j, drawtext = False))

def think(dt, controls):
	
#	self.inFbox0 = Fbox0.collidepoint(controls.mpos)
	self.mpos = controls.mpos
	self.ppos = view.FconvertB(Fspot0, controls.mpos)
	x, y = self.ppos
	self.inFbox0 = -0.06 < x < y / math.sqrt(3) + 0.06
#	if controls.mdown:
#		self.design.addcircle((x, y), 0.2, random.choice(["red", "orange", "yellow", "white", "green"]))
#		colors = ["#ffffff", "#ddddff", "#ddeeff"]
#		self.design.addshard(self.ppos, (0.06, 0.12), random.choice(colors))
#		self.design.addshape("blade", self.ppos, random.choice(colors), width = 0.01)
	background.update(dt, (20, 20, 60))
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
			else:
				for jstore, store in enumerate(self.store):
					if store[0].same(self.held):
						if store[1] is not None:
							store[1] += 1
						break
				else:
					print("Error restoring shape.")
			self.held = None
		checkcover()

	self.jbutton = None
	if not self.held and not self.inFbox0:
		for jbutton, button in enumerate(self.buttons):
			if button.contains(controls.mpos):
				self.jbutton = jbutton

	if self.jbutton is not None and controls.mdown:
		onclick(self.buttons[self.jbutton])

	if pygame.K_F5 in controls.kdowns:
		save()
	
	if not self.done and self.todo and not self.held:
		self.done = all(self.yescovers) and not any(self.nocovers)
	if self.done and not self.pushed:
		self.tdone = math.approach(self.tdone, 1, dt)
		if self.tdone == 1:
			self.pushed = True
			scene.pop()
			scene.push(winscene, self.design, Fspot1, self.stage)

def checkcover():
	self.yescovers = []
	for pos in self.yespoints:
		covered = self.design.colorat(pos)
		if self.held:
			covered = covered or self.held.colorat(render.tosector0(pos))
		self.yescovers.append(covered)


def onclick(button):
	if button.text == "Quit":
		scene.push(frostscene)
	if button.text == "Share":
		scene.push(uploadscene, self.design, Fspot1)
	if button.text.startswith("store-"):
		jstore = int(button.text[6:])
		shape, n = self.store[jstore]
		if n is not None and n <= 0:
			pass  # Error
		else:
			if n is not None:
				self.store[jstore][1] -= 1
			self.held = shape.copy()
			self.jheld = 0

def draw():
	if pview._fullscreen:
		pygame.mouse.set_visible(True)
	else:
		pygame.mouse.set_visible(not self.inFbox0 or self.held is None)
	background.draw()

	for jbutton, button in enumerate(self.buttons):
		note = None
		if button.text.startswith("store-"):
			jstore = int(button.text[6:])
			note = self.store[jstore][1]
			if note is not None:
				note = "%d" % note
		button.draw(lit = (jbutton == self.jbutton), note = note)
	self.design.drawwedge(Fspot0)
	self.design.draw(Fspot1)
	render.sector0(Fspot0)
	if self.inFbox0:
		render.sectors(Fspot1)
	
	for (x, y), covered in zip(self.yespoints, self.yescovers):
		p = view.BconvertF(Fspot1, (x, y))
		color = pygame.Color("#aaaaff" if covered else "#444488")
		ocolor = pygame.Color("white" if covered else "black")
		pygame.draw.circle(pview.screen, ocolor, T(p), T(8))
		pygame.draw.circle(pview.screen, color, T(p), T(6))
	if settings.DEBUG:
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

	if self.stage in stagedata.helptext:
		text = stagedata.helptext[self.stage]
		alpha = 0.3 if self.mpos[1] > 600 else 1
		ptext.draw(text, midbottom = T(640, 700), fontsize = T(38), width = T(1000), owidth = 0.5,
			fontname = "ChelaOne", color = "#ffffaa", shade = 1, shadow = (1, 1), alpha = alpha)

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


