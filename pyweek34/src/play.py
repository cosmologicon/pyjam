import pygame, math
from . import pview, maff, ptext
from . import landscape, control, view, graphics, sound, settings
from .pview import T

class Burner:
	def __init__(self, pos, r, lifetime, power):
		self.pos = pos
		self.r = r
		self.lifetime = lifetime
		self.power = power
		self.t = 0
		self.f = 0
		self.alive = True
	def think(self, dt):
		self.t += dt
		self.f = self.t / self.lifetime if self.lifetime else 1
		self.alive = self.t < self.lifetime
	def getdrains(self):
		yield self.pos, self.r, self.power
	def draw(self):
		for (xG, yG), rG, power in self.getdrains():
			pV = view.VconvertG(xG), view.VconvertG(yG)
			r = rG * math.dfade(self.t, 0, self.lifetime, 0.3)
			rV = view.VconvertG(0.2 * r)
			if not rV:
				continue
			graphics.drawat(graphics.sun(rV, self.t), pV)

class Wanderer(Burner):
	def __init__(self, pos0, pos1, r, speed, power):
		lifetime = (0.3 + math.distance(pos0, pos1)) / speed
		Burner.__init__(self, pos0, r, lifetime, power)
		self.pos0 = pos0
		self.pos1 = pos1
	def think(self, dt):
		Burner.think(self, dt)
		self.pos = math.mix(self.pos0, self.pos1, self.f)
		
class Spinner(Burner):
	def __init__(self, pos0, pos1, r, speed, power):
		lifetime = (0.3 + math.distance(pos0, pos1)) / speed
		Burner.__init__(self, pos0, r, lifetime, power)
		self.pos0 = pos0
		self.pos1 = pos1
		self.center = math.mix(self.pos0, self.pos1, 0.5)
		self.dpos = self.pos0[0] - self.center[0], self.pos0[1] - self.center[1]
		self.R = math.length(self.dpos)
	def think(self, dt):
		Burner.think(self, dt)
	def getdrains(self):
		dx, dy = math.R(-math.tau * self.f, self.dpos)
		cx, cy = self.center
		yield (cx + dx, cy + dy), self.r, self.power
		yield (cx - dx, cy - dy), self.r, self.power


class self:
	dmap = None

def init(level):
	self.level = level
	h0 = {
		1: 2.5,
		2: 2.5,
		3: 4,
	}[self.level]
	seed = self.level

	self.wG, self.hG = 16 / 9 * h0, h0
	PscaleG = 30 * settings.mapres / h0
	self.dmap = landscape.Dmap((self.wG, self.hG), PscaleG = PscaleG, seed = seed)
	view.SscaleG = pview.h0 / self.hG
	self.t = 0
	self.suns = []
	self.opts = []
	self.bindicator = None
	self.winning = False
	self.twin = 0
	if level == 1:
		self.tool = "basic"
		self.tools = ["basic"]
		self.recharge = { "basic": 3 }
	if level == 2:
		self.tool = "large"
		self.tools = ["large"]
		self.recharge = { "large": 3 }
	if level == 3:
		self.tool = "basic"
		self.tools = ["basic", "large"]
		self.recharge = { "basic": 5, "large": 5 }
	

	self.charge = { tool: self.recharge[tool] for tool in self.tools }
	

def think(dt, kdowns):
	self.t += dt
	click = control.getclick()
	dragging = control.getdragging()
	drop = control.getdrop()
	
	for tool in self.charge:
		self.charge[tool] = math.approach(self.charge[tool], self.recharge[tool], dt)

	if "swap" in kdowns:
		self.tool = self.tools[(self.tools.index(self.tool) + 1) % len(self.tools)]
		sound.play("swap")

	if click and self.tool in ("basic", "large"):
		if self.charge[self.tool] >= self.recharge[self.tool]:
			if self.tool == "basic":
				self.suns.append(Burner(view.GconvertVs(click), 1.5, 3, 2))
			if self.tool == "large":
				self.suns.append(Burner(view.GconvertVs(click), 4, 3, 0.5))
			self.charge[self.tool] = 0
		else:
			sound.play("no")

	if drop is not None:
		dropt, pdownV, pV = drop
		if self.tool == "burner" and self.bindicator is not None:
			if self.charge[self.tool] >= self.recharge[self.tool]:
				power = 2 * self.bindicator ** -1.2
				self.suns.append(Burner(view.GconvertVs(pV), self.bindicator, 3, power))
				self.charge["burner"] = 0
			else:
				sound.play("no")
#		self.suns.append(Spinner(view.GconvertVs(pdownV), view.GconvertVs(pV), 1, 2, 1))

	self.bindicator = None
	if dragging is not None:
		tdrag, pV0, pV1, ddrug = dragging
		if self.tool == "burner" and not ddrug:
			self.bindicator = math.mix(0.5, 2.5, math.cycle(0.5 * tdrag))
#	if click:
#		self.suns.append(Burner(view.GconvertVs(click), 1, 3, 0.3))
	
	for sun in self.suns:
		sun.think(dt)
		for (xG, yG), rG, power in sun.getdrains():
			self.dmap.drain(xG, yG, rG, power * dt)
	self.dmap.clip()
	self.suns = [sun for sun in self.suns if sun.alive]
	
	if self.dmap.fwater() <= 0.01 and not self.winning:
		self.winning = True
		sound.play("win")
	if self.winning:
		self.twin += dt

def won():
	return self.twin >= 1


def idist(x, x0, x1):
	return x0 - x if x < x0 else x - x1 if x > x1 else 0

def rectdist(rect, p):
	x, y = p
	return max(idist(x, rect.left, rect.right), idist(y, rect.top, rect.bottom))

def drawoverlay(text, **kwargs):
	surf, topleft = ptext.draw(text, surf = None, **kwargs)
	rect = surf.get_rect(topleft = topleft)
	d = rectdist(rect, control.pV)
	alpha = math.smoothfadebetween(d, 0, 0.2, T(30), 1)
	kwargs["alpha"] = kwargs.get("alpha", 1) * alpha
	ptext.draw(text, **kwargs)

def getinstructions():
	if self.level == 1:
		if self.dmap.fwater() > 0.4:
			return "Click to place solar radiation."
		if self.dmap.fwater() > 0.2:
			return "Tool cooldown shown in lower right."
		return "Get surface water below 1% to continue."
	if self.level == 2:
		return "Larger area of radiation is less concentrated."
	if self.level == 3:
		return "Press Tab or right click to swap between tools."


def draw():
	pview.fill((0, 0, 0))
	surf = self.dmap.tosurf()
	sizeV = view.VconvertG(self.wG), view.VconvertG(self.hG)
	surf = pygame.transform.smoothscale(surf, sizeV)
	pview.screen.blit(surf, (0, 0))
	for sun in self.suns:
		sun.draw()
	if self.bindicator is not None:
		rV = view.VconvertG(0.2 * self.bindicator)
		wV = view.VconvertG(0.05)
		color = (160, 160, 20) if self.charge[self.tool] >= self.recharge[self.tool] else (50, 50, 50)
		pygame.draw.circle(pview.screen, color, control.pV, rV, wV)


	title = {
		1: "Tutorial 1: Argyre Planitia",
		2: "Tutorial 2: Hesperia Planum",
		3: "Tutorial 3: Xanthe Terra",
	}[self.level]
	drawoverlay(title, midtop = T(640, 12), fontsize = T(48))
	instructions = getinstructions()
	if instructions is not None:
		drawoverlay(instructions, midbottom = T(640, 710), fontsize = T(26))
	info = [
		"Current: %s" % self.tool,
	]
	for tool in self.tools:
		info.append(f"{tool.upper()}: {self.charge[tool]:.1f}/{self.recharge[tool]:.1f}")
	drawoverlay("\n".join(info), bottomright = T(1270, 710), fontsize = T(26))

	alpha = int(max(math.interp(self.t, 0, 255, 0.5, 0), math.interp(self.twin, 0, 0, 1, 255)))
	if alpha:
		pview.fill((200, 50, 0, alpha))

