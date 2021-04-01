import math
import pygame
from . import enco, pview, ptext, settings, graphics
from . import view, state

tspawn0 = 3


class Lives(enco.Component):
	def __init__(self):
		self.alive = True
		self.t = 0
	def think(self, dt):
		self.t += dt

class Lifetime(enco.Component):
	def __init__(self, lifetime):
		self.f = 0
		self.lifetime = lifetime
	def think(self, dt):
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
		if math.hypot(*self.pG) > state.R + 1:
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
	def __init__(self):
		self.charge = 0
		self.meter = 0
	def arrive(self, bug):
		bug.alive = False
		if bug.jcolor == self.jcolor:
			self.charge += 1
		else:
			self.charge = 0
	def think(self, dt):
		self.charge *= 0.5 ** dt
		f = 1 - math.exp(-0.5 * dt / tspawn0)
		self.meter = math.mix(self.meter, math.log(2) * tspawn0 * self.charge, f)
	def draw(self):
		self.label("%.2f, %.2f" % (self.charge, self.meter))
	def charged(self):
		return self.meter > 2.5
	def overcharged(self):
		return self.meter > 3.5
	def getcolor(self):
		color = settings.colors[self.jcolor]
		if self.overcharged():
			return math.imix(color, (255, 255, 255), 0.5)
		if self.charged():
			return color
		return math.imix(color, (0, 0, 0), 0.5)


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
class Spawner:
	rG = 0.5
	color = 200, 200, 200
	def __init__(self, pH, tspawn, spec):
		self.pH = pH
		self.pG = view.GconvertH(self.pH)
		self.spec = spec
		self.bugtype = Ant
		self.tspawn = tspawn0
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
	def toggle(self):
		self.spec = [((dH + 1) % 6, jcolor) for dH, jcolor in self.spec]


@Lives()
@WorldBound()
class Tree:
	def __init__(self, pH, angle):
		self.pH = pH
		self.pG = view.GconvertH(self.pH)
		self.angle = angle
	def toggle(self):
		self.angle = -self.angle
	def draw(self):
		self.label("%d" % self.angle)

class Maple(Tree):
	color = 200, 0, 200
	rG = 0.2
	def direct(self, bug):
		assert bug.tile == self.pH
		dH = view.HrotH(bug.dH, self.angle)
		tile = view.vecadd(self.pH, dH)
		return tile, dH

class Oak(Tree):
	color = 255, 128, 0
	rG = 0.4
	def direct(self, bug):
		assert bug.tile == self.pH
		dH = view.HrotH(bug.dH, self.angle)
		tile = view.vecadd(self.pH, dH)
		return tile, bug.dH
	def draw(self):
		if self.t < 0.5:
			f = math.sqrt(self.t / 0.5)
			s = int(f * 20)
			angle = -100 * (1 - f)
		else:
			s, angle = 20, 0
		if s < 1:
			return
		scale = 0.0001 * s * view.cameraz
		graphics.drawimg(view.VconvertG(self.pG), "oak", scale = scale, angle = angle)

@WorldBound()
@Charges()
class Ring:
	def __init__(self, pH, jcolor, rH = 1):
		self.pH = pH
		self.pG = view.GconvertH(self.pH)
		self.rH = rH
		self.tiles = view.HsurroundH(self.pH, rH)
		self.jcolor = jcolor
		self.rG = [1.0, 2.4, 4, 5.6][rH]
	def toggle(self):
		self.jcolor = (self.jcolor + 1) % 3

