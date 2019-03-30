from __future__ import division
import random, math, pygame, json, os.path
from . import pview, flake, background, ptext, render, shape, view, hud, settings, client, sound
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
			self.store.append([shape.Shard((0, 0.5), "white", (0.06, 0.12)), None])
		if "Blade" in progress.shapes:
			self.store.append([shape.Blade((0, 0.5), "white", (0.02, 0.06)), None])
		if "Ring" in progress.shapes:
			self.store.append([shape.Ring((0, 0.5), "white", 0.03), None])
		if "Bar" in progress.shapes:
			self.store.append([shape.Bar((0, 0.5), "white", 0.03), None])
		if "Branch" in progress.shapes:
			self.store.append([shape.Branch((0.2, 0.6), "white", (0.03, 0.09)), None])
		if "Claw" in progress.shapes:
			self.store.append([shape.Claw((0, 0.5), "white", (0.06, 0.12)), None])
		if "Crown" in progress.shapes:
			self.store.append([shape.Crown((0.2, 0.5), "white", 0.04), None])
		if "Cusp" in progress.shapes:
			self.store.append([shape.Cusp((0.2, 0.5), "white", 0.04), None])
		if "Star" in progress.shapes:
			self.store.append([shape.Star((0, 0.5), "white", 0.12), None])
		for shp, n in self.store:
			shp.setksize(2)
	if stage in stagedata.store:
		for k, color, ksize, v in stagedata.store[stage]:
			if k == "Shard":
				shp = shape.Shard((0, 0.5), color, (0.06, 0.12))
			if k == "Blade":
				shp = shape.Blade((0, 0.5), color, (0.06, 0.12))
			if k == "Ring":
				shp = shape.Ring((0, 0.5), color, 0.03)
			if k == "Bar":
				shp = shape.Bar((0, 0.5), color, 0.03)
			if k == "Branch":
				shp = shape.Branch((0.2, 0.6), color, (0.06, 0.12))
			if k == "Claw":
				shp = shape.Claw((0, 0.5), color, (0.06, 0.12))
			if k == "Cusp":
				shp = shape.Cusp((0, 0.5), color, 0.04)
			if k == "Star":
				shp = shape.Star((0, 0.5), color, 0.12)
			shp.setksize(ksize)
			self.store.append([shp, v])
	self.maxshapes = progress.maxshapes if stage == "free" else None

	self.buttons = [
		hud.Button(((1200, 640), 50), "Quit"),
	]

	self.labels = []
	if self.stage == "free":
		if not settings.offline:
			self.buttons.append(hud.Button(((640, 640), 50), "Share"))
		if len(progress.colors) > 1:
			for jcolor, color in enumerate(progress.colors):
				Fspot = (180 + 23 * (jcolor % 2), 36 * jcolor + 60), 20
				text = "???" if color == "?" else "color-%s" % color
				drawtext = color == "?"
				bcolor = color if color != "?" else "#cccccc"
				self.buttons.append(hud.Button(Fspot, text, drawtext = drawtext, color = bcolor))
			self.labels.append(("Color", (180 + 23/2, 20)))
		if len(progress.sizes) > 1:
			y = 500
			for jsize, size in enumerate(progress.sizes):
				Fspot = (180 + 23 * (jsize % 2), y), 10 + 5 * size
				y += 25 + 10 * size
				self.buttons.append(hud.Button(Fspot, "size-%s" % size, drawtext = False))
			self.labels.append(("Size", (180 + 23/2, 460)))

	setpoints()
	self.todo = True
	self.done = False
	self.pushed = False
	self.tdone = 0


	for j, (shp, count) in enumerate(self.store):
		Fspot = (50 + 48 * (j % 2), 60 + 82 * j), 44
		self.buttons.append(hud.Button(Fspot, "store-%d" % j, drawtext = False, color = "#999999", shape = shp))
	
	self.ydata, self.ndata = [], []

	if "stage" in self.stage:
		sound.playmusic("twisting")
	else:
		sound.playmusic("techlive")

def setpoints():
	self.yespoints = []
	self.nopoints = []
	if self.stage in stagedata.points:
		yes, no = stagedata.points[self.stage]
		for a, r, n in yes:
			if settings.collapsepoints:
				n = 0
			if n % 2 == 1:
				a = 1 - a
			C, S = math.CS((n + a) / 12 * math.tau, r)
			self.yespoints.append((S, C))
		for a, r, n in no:
			if settings.collapsepoints:
				n = 0
			if n % 2 == 1:
				a = 1 - a
			C, S = math.CS((n + a) / 12 * math.tau, r)
			self.nopoints.append((S, C))
	checkcover()

def toggleeasy():
	settings.closepoints = not settings.closepoints
	settings.collapsepoints = settings.closepoints
	setpoints()

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
#	self.pointcolor = self.design.colorat(view.FconvertB(Fspot1, controls.mpos))
	self.pointcolor = None
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
		self.cursorimg = self.held.tobasic().cursorimg(T(100))
		self.design.undraw()

	if self.held:
		self.held.constrainanchor(self.jheld, self.ppos)
		if controls.mup:
			if self.inFbox0:
				self.design.shapes.append(self.held)
				self.design.undraw()
				sound.play("bonk")
			elif self.stage != "free":
				jstore = getjstore(self.held)
				store = self.store[jstore]
				if store[1] is not None:
					store[1] += 1
			self.held = None
		checkcover()

	self.jbutton = None
	if not self.held and not self.inFbox0:
		for jbutton, button in enumerate(self.buttons):
			if button.contains(controls.mpos):
				self.jbutton = jbutton

	if self.jbutton is not None and controls.mdown:
		onclick(self.buttons[self.jbutton])

	if pygame.K_TAB in controls.kdowns:
		toggleeasy()
	if settings.DEBUG:
		if pygame.K_F1 in controls.kdowns:
			self.done = True
		if pygame.K_F2 in controls.kdowns:
			addpoint(controls.mpos)
		if pygame.K_F5 in controls.kdowns:
			save()
		if pygame.K_F7 in controls.kdowns:
			randompoints()
	
	if not self.done and self.todo and not self.held:
		checkdone()
	if self.done and not self.pushed:
		self.tdone = math.approach(self.tdone, 1, dt)
		if self.tdone == 1:
			progress.beat(self.stage)
			self.pushed = True
			scene.pop()
			scene.push(winscene, self.design, Fspot1, self.stage)

def addpoint(pos):
	x, y = view.FconvertB(Fspot1, pos)
	r = math.length((x, y))
	na = 12 / math.tau * math.atan2(x, y)
	n, a = divmod(na, 1)
	n = int(n)
	if n % 2 == 1:
		a = 1 - a
	a = round(a, 3)
	r = round(r, 3)
	data = a, r, n

	if n % 2 == 1:
		a = 1 - a
	C, S = math.CS((n + a) / 12 * math.tau, r)
	pF = S, C
	covered = iscovered(pF)
	if covered:
		self.ydata += [data]
		self.yespoints += [pF]
	else:
		self.ndata += [data]
		self.nopoints += [pF]
	print()
	print([self.ydata, self.ndata])
	checkcover()
	

def randompoints():
	yout, nout = [], []
	self.yespoints = []
	self.nopoints = []
	for _ in range(16):
		a = random.uniform(0, 1)
		r = random.uniform(0, 1)
		n = 0
		if n % 2 == 1:
			a = 1 - a
		C, S = math.CS((n + a) / 12 * math.tau, r)
		pos = S, C
		covered = self.design.colorat(pos)
		if covered:
			self.yespoints.append((S, C))
			yout.append((a, r, n))
		else:
			self.nopoints.append((S, C))
			nout.append((a, r, n))
	print(yout)
	print(nout)
	checkcover()

def isred(color):
	r, g, b, a = ptext._resolvecolor(color, None)
	return r > 1.01 * g and r > 1.01 * b

def iscovered(pos):
	covered = self.design.colorat(pos)
	if self.held:
		heldcolor = self.held.colorat(render.tosector0(pos))
		if heldcolor:
			covered = heldcolor
	return not (covered is None or isred(covered))

def checkcover():
	self.yescovers = []
	self.nocovers = []
	for pos in self.yespoints:
		self.yescovers.append(iscovered(pos))
	for pos in self.nopoints:
		self.nocovers.append(iscovered(pos))

def checkdone():
	if self.stage == "free":
		return

	if self.stage == "stage1":
		self.done = self.store[0][1] == 0
	else:
		self.done = all(self.yescovers) and not any(self.nocovers)


def getjstore(shape):
	if self.stage == "free":
		return None
	for jstore, store in enumerate(self.store):
		if store[0].same(shape):
			return jstore
	print("Error restoring shape.")
	return None


def onclick(button):
	if button.text == "Quit":
		scene.push(frostscene, depth1 = 3)
		sound.play("fail")
	if button.text == "Share":
		if self.design.shapes:
			scene.push(uploadscene, self.design, Fspot1)
		sound.play("bonk")
	if button.text.startswith("store-"):
		jstore = int(button.text[6:])
		shape, n = self.store[jstore]
		shape = button.shape
		if n is not None and n <= 0:
			sound.play("no")
		elif self.maxshapes is not None and len(self.design.shapes) >= self.maxshapes:
			sound.play("no")
		else:
			if n is not None:
				self.store[jstore][1] -= 1
			self.held = shape.copy()
			self.cursorimg = self.held.cursorimg(T(100))
			self.jheld = 0
	if button.text.startswith("color-") or button.text == "???":
		sound.play("bonk")
		if "?" in button.text:
			color = "#" + "".join(random.choice("89abcdef") for _ in range(6))
		else:
			color = tuple(pygame.Color(button.text[6:]))
			colors = [math.imix(color, (255, 255, 255, 255), a) for a in (0, 0.2, 0.4, 0.6, 0.8)]
			colornow = tuple([button.shape.color for button in self.buttons if button.text == "store-0"][0])
			if colornow in colors:
				color = colors[(colors.index(colornow) + 1) % len(colors)]
			else:
				color = colors[0]
		for button in self.buttons:
			if button.text.startswith("store-"):
				shape = button.shape.copy()
				shape.color = color
				button.setshape(shape)
	if button.text.startswith("size-"):
		sound.play("bonk")
		ksize = int(button.text[5:])
		for button in self.buttons:
			if button.text.startswith("store-"):
				shape = button.shape.copy()
				shape.setksize(ksize)
				button.setshape(shape)

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
		if self.maxshapes is not None and len(self.design.shapes) >= self.maxshapes:
			note = ""
		button.draw(lit = (jbutton == self.jbutton), note = note)
	self.design.drawwedge(Fspot0)
	self.design.draw(Fspot1)
	render.sector0(Fspot0)
	if self.inFbox0:
		render.sectors(Fspot1)

	for text, pos in self.labels:
		ptext.draw(text, center = T(pos), fontsize = T(30),
			color = "#ffffaa", fontname = "ChelaOne",
			shade = 1, owidth = 0.4, shadow = (1, 1))

	Fspot = Fspot0 if settings.closepoints else Fspot1	
	a = math.cycle(pygame.time.get_ticks() / 500)
	offcolor = pygame.Color(*math.imix((50, 50, 100), (100, 100, 255), a))
	for (x, y), covered in zip(self.yespoints, self.yescovers):
		p = view.BconvertF(Fspot, (x, y))
		color = pygame.Color("#aaaaff") if covered else offcolor
		ocolor = pygame.Color("black" if covered else "white")
		pygame.draw.circle(pview.screen, ocolor, T(p), T(8))
		pygame.draw.circle(pview.screen, color, T(p), T(6))
	oncolor = pygame.Color(*math.imix((100, 50, 50), (255, 100, 100), a))
	for (x, y), covered in zip(self.nopoints, self.nocovers):
		p = view.BconvertF(Fspot, (x, y))
		color = oncolor if covered else pygame.Color("#884444")
		ocolor = pygame.Color("white" if covered else "black")
		rect = T(pygame.Rect(0, 0, 16, 16))
		rect.center = T(p)
		pygame.draw.rect(pview.screen, ocolor, rect)
		rect = T(pygame.Rect(0, 0, 12, 12))
		rect.center = T(p)
		pygame.draw.rect(pview.screen, color, rect)
	if settings.DEBUG:
		ptext.draw(str(self.pointcolor), bottomright = T(1260, 710), fontsize = T(30))

	if self.yespoints:
		n = len(self.yescovers)
		a = sum(self.yescovers)
		text = "Remaining: %d/%d" % (n - a, n)
		ptext.draw(text, topright = T(1280, 0), fontsize = T(38), owidth = 0.5,
			fontname = "ChelaOne", color = "#ccccff", shade = 0.5, shadow = (1, 1))
	if self.nopoints:
		n = len(self.nocovers)
		a = sum(self.nocovers)
		text = "Covered: %d/%d" % (a, n)
		ptext.draw(text, topright = T(1280, 38), fontsize = T(38), owidth = 0.5,
			fontname = "ChelaOne", color = "#ffcccc", shade = 0.5, shadow = (1, 1))
	if (self.yespoints or self.nopoints) and settings.closepoints:
		ptext.draw("EASY MODE: ON", topleft = T(10, 500), fontsize = T(30),
			color = "#ffffaa", fontname = "ChelaOne",
			shade = 1, owidth = 0.4, shadow = (1, 1))

	if self.maxshapes is not None:
		text = "Shapes used: %d/%d" % (len(self.design.shapes), self.maxshapes)
		ptext.draw(text, topright = T(1280, 0), fontsize = T(38), owidth = 0.5,
			fontname = "ChelaOne", color = "#ffffff", shade = 0.5, shadow = (1, 1))

	if self.held and self.inFbox0:
		for j, anchor in enumerate(self.held.anchors):
			color = "white" if j == self.jheld else "orange"
			render.anchor(Fspot0, anchor, color)
		self.held.drawoutline0(Fspot0)
		self.held.drawoutline(Fspot1)
	else:
		if self.held:
			rect = self.cursorimg.get_rect(center = T(self.mpos))
			pview.screen.blit(self.cursorimg, rect)
		for i, j, anchor in self.design.anchors():
			color = "white" if (i, j) == self.panchor else "orange"
			render.anchor(Fspot0, anchor, color)

	if self.stage in stagedata.helptext:
		text = stagedata.helptext[self.stage]
		alpha = 0.3 if self.mpos[1] > 600 else 1
		ptext.draw(text, midbottom = T(640, 700), fontsize = T(38), width = T(1000), owidth = 0.5,
			fontname = "ChelaOne", color = "#ffffaa", shade = 1, shadow = (1, 1), alpha = alpha)

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


