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
		4: 3,
		5: 3,
		6: 10,
		7: 16,
	}[self.level]
	seed = self.level

	self.wG, self.hG = 16 / 9 * h0, h0
	PscaleG = 30 * settings.mapres / h0
	self.dmap = landscape.Dmap((self.wG, self.hG), PscaleG = PscaleG, seed = seed)
	self.dmap.drain(0.92 * self.wG, 0.92 * self.hG, 0.33 * self.hG, 6)
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
	if level == 4:
		self.tool = "wander"
		self.tools = ["wander"]
		self.recharge = { "wander": 3 }
	if level == 5:
		self.tool = "spin"
		self.tools = ["spin"]
		self.recharge = { "spin": 3 }
	if level == 6:
		self.tool = "basic"
		self.tools = ["basic", "large", "wander", "spin"]
		self.recharge = { "basic": 10, "large": 10, "wander": 10, "spin": 10 }
	if level == 7:
		self.tool = "basic"
		self.tools = ["basic", "large", "wander", "spin"]
		self.recharge = { "basic": 4, "large": 4, "wander": 4, "spin": 4 }
	self.hudrects = [pygame.Rect(1090, 680 - 40 * j, 180, 30) for j in range(len(self.tools))][::-1]

	self.charge = { tool: self.recharge[tool] for tool in self.tools }
	self.comets = []
	self.jcomet = 0

	sound.playmusic("martian-cowboy")
	if self.level == 7:
		sound.playmusic("enter-the-party")

def canuse(tool):
	return self.charge[tool] >= self.recharge[tool]

def think(dt, kdowns):
	self.t += dt
	click = control.getclick()
	dragging = control.getdragging()
	drop = control.getdrop()
	
	for tool in self.charge:
		self.charge[tool] += dt

	if "swap" in kdowns:
		self.tool = self.tools[(self.tools.index(self.tool) + 1) % len(self.tools)]
		sound.play("swap")
	for j, tool in enumerate(self.tools, 1):
		if f"tool{j}" in kdowns and tool != self.tool:
			self.tool = tool
			sound.play("swap")
	if control.getrclick():
		chargemax = max(self.charge.values())
		tool = next(tname for tname, charge in self.charge.items() if charge == chargemax)
		if tool != self.tool:
			sound.play("swap")
			self.tool = tool

	if click:
		for hudrect, tool in zip(self.hudrects, self.tools):
			if T(hudrect).collidepoint(control.pV):
				sound.play("click" if self.tool == tool else "swap")
				self.tool = tool
				break
		else:
			if self.tool in ("basic", "large"):
				if canuse(self.tool):
					if self.tool == "basic":
						self.suns.append(Burner(view.GconvertVs(click), 1.5, 3, 2))
						sound.play("use-basic")
					if self.tool == "large":
						self.suns.append(Burner(view.GconvertVs(click), 4, 3, 0.5))
						sound.play("use-large")
					self.charge[self.tool] = 0
				else:
					sound.play("no")

	if drop is not None:
		dropt, pdownV, pV = drop
		if self.tool in ("wander", "spin"):
			if canuse(self.tool):
				pos0 = view.GconvertVs(pdownV)
				pos1 = view.GconvertVs(pV)
				if self.tool == "wander":
					self.suns.append(Wanderer(pos0, pos1, 1.5, 0.7, 1.2))
					sound.play("use-wander")
				if self.tool == "spin":
					self.suns.append(Spinner(pos0, pos1, 1.5, 0.7, 1.2))
					sound.play("use-spin")
				self.charge[self.tool] = 0
			else:
				sound.play("no")
			
			
		if self.tool == "burner" and self.bindicator is not None:
			if canuse(self.tool):
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

	tcomet = 2 if self.level == 7 else 20
	nextcomet = tcomet * (self.jcomet + 1) ** 0.9
	if self.level in (6, 7) and self.t >= nextcomet:
		x = math.fuzzrange(0.15, 0.85, self.jcomet, 17) * self.wG
		y = math.fuzzrange(0.15, 0.85, self.jcomet, 18) * self.hG
		self.comets.append([-3, x, y])
		self.jcomet += 1

	
	for sun in self.suns:
		sun.think(dt)
		for (xG, yG), rG, power in sun.getdrains():
			self.dmap.drain(xG, yG, rG, power * dt)
	for comet in self.comets:
		t, x, y = comet
		if t < 0 and t + dt >= 0:
			if self.level != 7:
				sound.play("comet")
			t, x, y = comet
		t += dt
		comet[0] = t
		if 0 < t < 1:
			r = 1.5 * (t / 1.0) ** 0.4
			power = 20.0 * (t / 1.0) ** 4
			self.dmap.drain(x, y, r + 0.5, power * dt)
			self.dmap.drain(x, y, r, -1.6 * power * dt)

	self.dmap.clip()
	self.suns = [sun for sun in self.suns if sun.alive]
	self.comets = [comet for comet in self.comets if comet[0] < 10]
	
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
		return "Click to place solar radiation.\nTool cooldown shown in lower right.\nGet surface to less than 1% ocean to continue."
	if self.level == 2:
		return "Sunspread is less concentrated but covers a larger area.\nSee README for options, full controls, and cheats."
	if self.level == 3:
		return "Use Tab or number keys to switch between tools."
	if self.level == 4:
		return "Click and drag a path to use Sunbeam."
	if self.level == 5:
		return "Click and drag diameter to use Sunwheel."
	if self.level == 6:
		return "Tab cycles between tools.\nRight click swaps to tool with highest charge."
	if self.level == 7:
		return "Optional final level. Thank you for playing."

def draw():
	pview.fill((0, 0, 0))
	surf = self.dmap.tosurf()
	sizeV = view.VconvertG(self.wG), view.VconvertG(self.hG)
	surf = pygame.transform.smoothscale(surf, sizeV)
	pview.screen.blit(surf, (0, 0))
	for t, x, y in self.comets:
		if t >= 0: continue
		pos = view.VconvertG(x), view.VconvertG(y)
		rV = view.VconvertG(1 - t % 1)
		wV = view.VconvertG(0.02)
		if wV < rV:
			pygame.draw.circle(pview.screen, (40, 100, 160), pos, rV, wV)
		
	for sun in self.suns:
		sun.draw()
	color = (160, 160, 20) if canuse(self.tool) else (50, 50, 50)
	if control.self.pressed:
		drag = control.getdragging()
		if drag is not None and self.tool in ("wander", "spin"):
			tdrag, pV0, pV1, ddrug = drag
			if math.distance(pV0, pV1) > 10:
				pygame.draw.line(pview.screen, color, pV0, pV1, view.VconvertG(0.02))
	else:
		if self.tool == "basic":
			rV = view.VconvertG(1.5/8)
			wV = view.VconvertG(0.02)
			pygame.draw.circle(pview.screen, color, control.pV, rV, wV)
		elif self.tool == "large":
			rV = view.VconvertG(4/8)
			wV = view.VconvertG(0.01)
			pygame.draw.circle(pview.screen, color, control.pV, rV, wV)
		elif self.tool == "wander":
			dx = view.VconvertG(0.1)
			dy = view.VconvertG(0.2)
			x0, x1 = control.xV - dx, control.xV + dx
			y0, y1 = control.yV - dy, control.yV + dy
			wV = view.VconvertG(0.02)
			pygame.draw.line(pview.screen, color, (x0, y0), (x0, y1), wV)
			pygame.draw.line(pview.screen, color, (x1, y0), (x1, y1), wV)
		elif self.tool == "spin":
			rV = view.VconvertG(1.5/8)
			rect = pygame.Rect(0, 0, 2 * rV, 2 * rV)
			rect.center = control.pV
			a0 = self.t * 2 % math.tau
			wV = view.VconvertG(0.01)
			pygame.draw.arc(pview.screen, color, rect, a0, a0 + math.tau / 4, wV)
			pygame.draw.arc(pview.screen, color, rect, a0 + math.tau / 2, a0 + 3 * math.tau / 4, wV)

	if self.bindicator is not None:
		rV = view.VconvertG(0.2 * self.bindicator)
		wV = view.VconvertG(0.05)
		color = (160, 160, 20) if self.charge[self.tool] >= self.recharge[self.tool] else (50, 50, 50)
		pygame.draw.circle(pview.screen, color, control.pV, rV, wV)


	title = {
		1: "Tutorial 1: Argyre Planitia",
		2: "Tutorial 2: Hesperia Planum",
		3: "Tutorial 3: Xanthe Terra",
		4: "Tutorial 4: Terra Sirenum",
		5: "Tutorial 5: Arcadia Planitia",
		6: "Challenge: Vastitas Borealis",
		7: "The End: Utopia Planitia",
	}[self.level]
	drawoverlay(title, midtop = T(640, 12), fontsize = T(48))
	instructions = getinstructions()
	if instructions is not None:
		drawoverlay(instructions, midbottom = T(640, 710), fontsize = T(26))
	for j, (hudrect, tool) in enumerate(zip(self.hudrects, self.tools)):
		bcolor = (100, 100, 255) if tool == self.tool else (0, 0, 0)
		pygame.draw.rect(pview.screen, bcolor, T(hudrect).inflate(T(9), T(9)))
		f = math.clamp(self.charge[tool] / self.recharge[tool], 0, 1)
		if f < 1:
			pygame.draw.rect(pview.screen, (80, 80, 80), T(hudrect))
		barrect = pygame.Rect(T(hudrect))
		barrect.width = T(f * hudrect.width)
		pygame.draw.rect(pview.screen, (240, 240, 240), barrect)
		tname = {
			"basic": "Sunspot",
			"large": "Sunspread",
			"wander": "Sunbeam",
			"spin": "Sunwheel",
		}[tool]
		color = (240, 240, 240) if canuse(tool) else (80, 80, 80)
		ptext.draw(f"{j+1}: {tname}", center = T(hudrect.center), color = color, fontsize = T(24))

	hud = f"{100 * self.dmap.fwater():.1f}% ocean\n{10 * self.t:.0f} million years"
	drawoverlay(hud, bottomleft = T(10, 710), fontsize = T(40))
#	info = [
#		"Current: %s" % self.tool,
#	]
#	for tool in self.tools:
#		info.append(f"{tool.upper()}: {self.charge[tool]:.1f}/{self.recharge[tool]:.1f}")
#	drawoverlay("\n".join(info), bottomright = T(1270, 710), fontsize = T(26))

	alpha = int(max(math.interp(self.t, 0, 255, 0.5, 0), math.interp(self.twin, 0, 0, 1, 255)))
	if alpha:
		pview.fill((200, 50, 0, alpha))

