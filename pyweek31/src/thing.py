import math
import pygame
from . import enco, pview, ptext, settings
from . import view, state

class Lives(enco.Component):
	def __init__(self):
		self.alive = True

class Lifetime(enco.Component):
	def __init__(self, lifetime):
		self.t = 0
		self.f = 0
		self.lifetime = lifetime
	def think(self, dt):
		self.t += dt
		self.f = math.clamp(self.t / self.lifetime, 0, 1)
		if self.f == 1:
			self.alive = False

class WorldBound(enco.Component):
	def __init__(self):
		self.pG = 0, 0
		self.rG = 0.25
	def getcolor(self):
		if hasattr(self, "color"): return self.color
		return settings.colors[self.jcolor]
	def draw(self):
		pV = view.VconvertG(self.pG)
		rV = view.VscaleG(self.rG)
		pygame.draw.circle(pview.screen, self.getcolor(), pV, rV)
	def think(self, dt):
		if math.hypot(*self.pG) > 30:
			self.alive = False
	def label(self, text):
		ptext.draw(text, center = view.VconvertG(self.pG), fontsize = view.VscaleG(1), owidth = 1)
	def drawarrow(self, color, jdH):
		dGs = [math.R(-jdH * math.tau / 6, p) for p in [(0, 1), (0.3, 0.8), (-0.3, 0.8)]]
		pVs = [view.VconvertG(view.vecadd(self.pG, dG)) for dG in dGs]
		pygame.draw.polygon(pview.screen, color, pVs)


class Travels(enco.Component):
	def __init__(self, speed):
		self.tile = 0, 0
		self.dH = 0, 0
		self.speed = 1
		self.ftravel = 0
	def think(self, dt):
		self.ftravel += self.speed * dt
		while self.ftravel >= 1:
			self.ftravel -= 1
			self.advance()
		pG0 = view.GconvertH(view.vecadd(self.tile, self.dH, -0.5))
		pG1 = view.GconvertH(view.vecadd(self.nexttile, self.nextdH, -0.5))
		self.pG = math.mix(pG0, pG1, self.ftravel)
	def advance(self):
		self.tile = self.nexttile
		self.dH = self.nextdH
		self.setnext()
	def setnext(self):
		tree = state.treeat(self.tile)
		if tree is None:
			self.nexttile = view.vecadd(self.tile, self.dH)
			self.nextdH = self.dH
		else:
			self.nexttile, self.nextdH = tree.direct(self)
		ring = state.ringat(self.tile)
		if ring is not None:
			ring.arrive(self)
	def draw(self):
		self.drawarrow(self.getcolor(), view.dirHs.index(self.dH))
		
class Charges(enco.Component):
	def __init__(self, maxcharge):
		self.charge = 0
		self.maxcharge = maxcharge
		self.dcharge = -1
	def arrive(self, bug):
		bug.alive = False
		if bug.jcolor == self.jcolor:
			self.charge += 1
		else:
			self.charge -= 1
		self.charge = math.clamp(self.charge, 0, self.maxcharge)
	def think(self, dt):
		self.charge += dt * self.dcharge
		self.charge = math.clamp(self.charge, 0, self.maxcharge)
	def draw(self):
		self.label("%d/%d" % (int(self.charge), self.maxcharge))


@Lives()
@WorldBound()
@Travels(1)
class Ant:
	def __init__(self, pH, dH, jcolor):
		self.tile = pH
		self.dH = dH
		self.jcolor = jcolor
		self.setnext()

@WorldBound()
class BugSpawner:
	rG = 0.5
	def __init__(self, pH, dH, bugtype, color, tspawn):
		self.pH = pH
		self.pG = view.GconvertH(self.pH)
		self.dH = dH
		self.bugtype = bugtype
		self.color = color
		self.tspawn = tspawn
		self.t = 0
	def think(self, dt):
		self.t += dt
		while self.t > self.tspawn:
			self.t -= self.tspawn
			bug = self.bugtype(self.pH, self.dH, color = self.color)
			bug.advance()
			state.bugs.append(bug)
		
@WorldBound()
class MultiSpawner:
	rG = 0.5
	color = 200, 200, 200
	def __init__(self, pH, tspawn, spec):
		self.pH = pH
		self.pG = view.GconvertH(self.pH)
		self.spec = spec
		self.bugtype = Ant
		self.tspawn = tspawn
		self.t = 0
	def think(self, dt):
		self.t += dt
		while self.t > self.tspawn:
			self.t -= self.tspawn
			for jdH, jcolor in self.spec:
				bug = self.bugtype(self.pH, view.dirHs[jdH%6], jcolor)
				bug.advance()
				state.bugs.append(bug)
	def draw(self):
		for dH, jcolor in self.spec:
			self.drawarrow(settings.colors[jcolor], dH)


@WorldBound()
class Maple:
	color = 200, 0, 200
	def __init__(self, pH, angle):
		self.pH = pH
		self.pG = view.GconvertH(self.pH)
		self.angle = angle
	def toggle(self):
		self.angle = -self.angle
	def direct(self, bug):
		assert bug.tile == self.pH
		dH = view.HrotH(bug.dH, self.angle)
		tile = view.vecadd(self.pH, dH)
		return tile, dH
	def draw(self):
		self.label("%d" % self.angle)

@WorldBound()
class Oak:
	color = 255, 128, 0
	rG = 0.35
	def __init__(self, pH, angle):
		self.pH = pH
		self.pG = view.GconvertH(self.pH)
		self.angle = angle
	def toggle(self):
		self.angle = -self.angle
	def direct(self, bug):
		assert bug.tile == self.pH
		dH = view.HrotH(bug.dH, self.angle)
		tile = view.vecadd(self.pH, dH)
		return tile, bug.dH
	def draw(self):
		self.label("%d" % self.angle)

@WorldBound()
@Charges(10)
class ChargeRing:
	def __init__(self, pH, jcolor, rH = 1):
		self.pH = pH
		self.pG = view.GconvertH(self.pH)
		self.rH = rH
		self.tiles = view.HsurroundH(self.pH, rH)
		self.jcolor = jcolor
		self.rG = [1.0, 2.4, 4, 5.6][rH]

