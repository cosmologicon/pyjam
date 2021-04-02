import math, random
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
#		pygame.draw.circle(pview.screen, self.getcolor(), pV, rV)
	def label(self, text):
		ptext.draw(text, center = view.VconvertG(self.pG), fontsize = view.VscaleG(1), owidth = 1)
	def drawarrow(self, color, jdH):
		dGs = [math.R(-jdH * math.tau / 6, p) for p in [(0, 1), (0.3, 0.8), (-0.3, 0.8)]]
		pVs = [view.VconvertG(view.vecadd(self.pG, dG)) for dG in dGs]
		pygame.draw.polygon(pview.screen, color, pVs)


class Bounded(enco.Component):
	def __init__(self, dR = 1):
		self.dR = dR
	def think(self, dt):
		if math.hypot(*self.pG) > state.R + self.dR:
			self.alive = False
			state.ghosts.append(OuterGhost(self))


class Travels(enco.Component):
	def __init__(self, speed):
		self.tile = 0, 0
		self.dH = 0, 0
		self.speed = 1
		self.ftravel = 0
	def think(self, dt):
		if self.guider is None:
			self.ftravel += self.speed * dt
			pG0 = view.GconvertH(view.vecadd(self.tile, self.dH, -0.5))
			pG1 = view.GconvertH(view.vecadd(self.nexttile, self.nextdH, -0.5))
			self.pG = math.mix(pG0, pG1, self.ftravel)
		else:
			self.guider.guide(self, dt)
		while self.ftravel >= 1:
			self.ftravel -= 1
			self.advance()
	def advance(self):
		self.tile = self.nexttile
		self.dH = self.nextdH
		self.setnext()

class Arrives(enco.Component):
	def setnext(self):
		tree = state.treeat(self.tile)
		if tree is None:
			self.nexttile = view.vecadd(self.tile, self.dH)
			self.nextdH = self.dH
			self.guider = None
		else:
			tree.direct(self)
			self.guider = tree
		ring = state.ringat(self.tile)
		if ring is not None:
			ring.arrive(self)
			state.ghosts.append(RingGhost(self, ring))
#	def draw(self):
#		self.drawarrow(self.getcolor(), view.dirHs.index(self.dH))

class DoesntArrive(enco.Component):
	def setnext(self):
		self.nexttile = view.vecadd(self.tile, self.dH)
		self.nextdH = self.dH


class Tracks(enco.Component):
	def think(self, dt):
		self.pG = view.vecadd(self.pG, self.vG, dt)

class Trails(enco.Component):
	def __init__(self):
		self.trailers = []
		self.nexttrailer = 0
	def think(self, dt):
		if self.t >= self.nexttrailer:
			self.nexttrailer = self.t + random.uniform(0.2, 0.3)
			pG = view.vecadd(self.pG, (random.uniform(-1, 1), random.uniform(-1, 1)), 0.1)
			self.trailers.append((self.t, pG))
			self.trailers = [(t, p) for t, p in self.trailers if self.t - t < 1]
	def draw(self):
		color, alpha0 = self.getcolor(), 255
		if len(color) > 3:
			color, alpha0 = color[0:3], color[3]
		graphics.drawsprite(view.VconvertG(self.pG), view.VscaleG(0.6), color + (alpha0,))
		for t, p in self.trailers:
			f = (self.t - t) * 2
			alpha = int(math.imix(10, 0, f) * alpha0 / 10)
			if alpha > 0:
				graphics.drawsprite(view.VconvertG(p), view.VscaleG(0.5), color + (alpha,))


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
		if settings.DEBUG:
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
@Bounded()
@Travels(1)
@Arrives()
@Trails()
class Ant:
	def __init__(self, pH, dH, jcolor):
		self.tile = pH
		self.dH = dH
		self.jcolor = jcolor
		self.setnext()
		self.trailers = []
		self.nexttrailer = 0
	def think(self, dt):
		if self.t >= self.nexttrailer:
			self.nexttrailer = self.t + random.uniform(0.2, 0.3)
			pG = view.vecadd(self.pG, (random.uniform(-1, 1), random.uniform(-1, 1)), 0.1)
			self.trailers.append((self.t, pG))
			self.trailers = [(t, p) for t, p in self.trailers if self.t - t < 1]

@Lives()
@Lifetime(1)
@WorldBound()
@Tracks()
@Trails()
class OuterGhost:
	def __init__(self, ant):
		self.jcolor = ant.jcolor
		self.pG = ant.pG
		self.vG = math.norm(view.GconvertH(ant.dH), ant.speed)
		self.trailers = [(t - ant.t, p) for t, p in ant.trailers]
		self.nexttrailer = ant.nexttrailer - ant.t
	def getcolor(self):
		color = settings.colors[self.jcolor]
		alpha = math.imix(255, 0, self.f)
		return color + (alpha,)

@Lives()
@Lifetime(13)
@WorldBound()
@Tracks()
@Trails()
class RingGhost:
	def __init__(self, ant, ring):
		self.jcolor = ant.jcolor
		self.pG = ant.pG
		self.ring = ring
		self.speed = ant.speed
		self.vG0 = math.norm(view.GconvertH(ant.dH), ant.speed)
		self.vG = self.vG0
		self.trailers = [(t - ant.t, p) for t, p in ant.trailers]
		self.nexttrailer = ant.nexttrailer - ant.t
	def getcolor(self):
		color = settings.colors[self.jcolor]
		alpha = int(math.fadebetween(self.t, 11, 255, 13, 0))
		return color + (alpha,)
	def think(self, dt):
		dx, dy = view.vecadd(self.pG, self.ring.pG, -1)
		r = math.hypot(dx, dy)
		r0 = math.smoothfadebetween(self.t, 6, 1.5, 13, 0.1)
		vG = view.vecadd(
			math.norm((dy, -dx), self.speed if self.jcolor == self.ring.jcolor else -self.speed),
			math.norm((dx, dy)), -(r - r0))
		self.vG = math.fadebetween(self.t, 0, self.vG0, 4, vG)


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
		pV = view.VconvertG(self.pG)
		scale = 1.2 + (0.2 * math.sin(self.t * 20 * math.tau) if self.t < 0.1 else 0)
		scale = view.VscaleG(scale) / 400
		angle = 1
		graphics.drawimg(pV, "shroom-0", scale = scale, angle = angle, cmask = (120, 120, 120))
#		for dH, jcolor in self.spec:
#			self.drawarrow(settings.colors[jcolor], dH)
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
	def drawroots(self):
		f = math.mix(0, 1, self.t)
		graphics.drawroots(view.VconvertG(self.pG), view.VscaleG(2.2), self.color, f)
	def draw(self):
		if self.t < 0.5:
			f = math.sqrt(self.t / 0.5)
			s = int(f * 20)
			angle = -100 * (1 - f)
		else:
			s, angle = 20, 0
		if s < 1:
			return
		scale = 0.00025 * self.rG * s * view.cameraz
		graphics.drawimg(view.VconvertG(self.pG), self.imgname, scale = scale, angle = angle)
		for dpG in math.CSround(3, 0.6, 2 * self.t * self.angle):
			pG = view.vecadd(self.pG, dpG)
			graphics.drawsprite(view.VconvertG(pG), view.VscaleG(0.3), (255, 255, 255, 100))
#		self.label("%d" % self.angle)

class Oak(Tree):
	color = 100, 60, 20
	rG = 0.36
	imgname = "oak"
	def direct(self, bug):
		bug.nexttile = view.vecadd(self.pH, view.HrotH(bug.dH, self.angle))
		bug.nextdH = bug.dH
		bug.Rguide = 1
		dx, dy = math.norm(view.GconvertH(bug.dH), bug.Rguide)
		bug.xhat = (dy, -dx) if self.angle > 0 else (-dy, dx)
		bug.yhat = dx, dy
		bug.guide0 = view.vecadd(view.GconvertH(view.vecadd(bug.nexttile, bug.nextdH, -0.5)), bug.xhat, -1)
	def guide(self, bug, dt):
		bug.ftravel += math.sqrt(3) * bug.speed * dt / bug.Rguide / (math.tau / 3)
		C, S = math.CS((1 - bug.ftravel) * math.tau / 3)
		bug.pG = view.vecadd(view.vecadd(bug.guide0, bug.xhat, C), bug.yhat, -S)
		

class Beech(Tree):
	color = 200, 180, 160
	rG = 0.3
	imgname = "beech"
	def direct(self, bug):
		bug.nextdH = view.HrotH(bug.dH, self.angle)
		bug.nexttile = view.vecadd(self.pH, bug.nextdH)
		bug.Rguide = 1.5
		dx, dy = math.norm(view.GconvertH(bug.dH), bug.Rguide)
		bug.xhat = (-dy, dx) if self.angle > 0 else (dy, -dx)
		bug.yhat = dx, dy
		bug.guide0 = view.vecadd(view.GconvertH(view.vecadd(bug.tile, bug.dH, -0.5)), bug.xhat, -1)
	def guide(self, bug, dt):
		bug.ftravel += math.sqrt(3) * bug.speed * dt / bug.Rguide / (math.tau / 6)
		C, S = math.CS(bug.ftravel * math.tau / 6)
		bug.pG = view.vecadd(view.vecadd(bug.guide0, bug.xhat, C), bug.yhat, S)

class Pine(Tree):
	color = 160, 130, 80
	rG = 0.3
	imgname = "pine"
	def direct(self, bug):
		bug.nextdH = view.HrotH(bug.dH, self.angle)
		bug.nexttile = view.vecadd(self.pH, bug.nextdH)
		bug.Rguide = 0.5
		dx, dy = math.norm(view.GconvertH(bug.dH), bug.Rguide)
		bug.xhat = (-dy, dx) if self.angle > 0 else (dy, -dx)
		bug.yhat = dx, dy
		bug.guide0 = view.vecadd(view.GconvertH(view.vecadd(bug.tile, bug.dH, -0.5)), bug.xhat, -1)
	def guide(self, bug, dt):
		bug.ftravel += math.sqrt(3) * bug.speed * dt / bug.Rguide / (math.tau / 3)
		C, S = math.CS(bug.ftravel * math.tau / 3)
		bug.pG = view.vecadd(view.vecadd(bug.guide0, bug.xhat, C), bug.yhat, S)


@Lives()
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
	def draw(self):
		xG0, yG0 = self.pG
		fcharge = math.fadebetween(self.meter, 0, -1, 2.5, 1)
		color0 = settings.colors[self.jcolor]
		if self.meter < 3:
			fcharge = math.fadebetween(self.meter, 2, 0, 2.5, 1)
			fcharge = int(fcharge * 5) / 5
			color = math.imix((0, 0, 0), color0, 0.4 + 0.6 * fcharge)
		else:
			fcharge = math.fadebetween(self.meter, 3.5, 0, 4, 1)
			fcharge *= math.cycle(self.t)
			fcharge = int(fcharge * 5) / 5
			color = math.imix(color0, (255, 255, 255), fcharge)
		for j, (dxG, dyG) in enumerate(math.CSround(13, 0.86 * self.rG, 0.1 * xG0 + 0.2 * yG0)):
			j += 1.23 + xG0 * yG0 + 0.7 * xG0 - 0.3 * yG0
			xG = xG0 + dxG + math.mix(-0.2, 0.2, math.phi * j % 1)
			yG = yG0 + dyG + math.mix(-0.2, 0.2, math.phi ** 2 * j % 1)
			a = math.mix(0.6, 1, 0.71 * j % 1)
			scale = view.VscaleG(a) / 400
			angle = 360 * math.phi * j
			iname = "shroom-0" if angle % 1 < 0.5 else "shroom-1"
			graphics.drawimg(view.VconvertG((xG, yG)), iname, scale = scale, angle = angle, cmask = color)



