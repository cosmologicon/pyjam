import pygame, math, random
from . import view, grid, pview, effects, state, fuzz, graphics, sound
from .pview import T

class Oscillator:
	def __init__(self, A, omega0, omega1, *seed):
		self.A = A
		self.omega = fuzz.uniform(omega0, omega1, 0, *seed)
		self.phi = fuzz.uniform(0, math.tau, 1, *seed)
	def __call__(self, t):
		return self.A * math.sin(self.omega * t + self.phi)

class Lissajous:
	def __init__(self, A, omega0, omega1, *seed):
		self.dx = Oscillator(A, omega0, omega1, 100, *seed)
		self.dy = Oscillator(A, omega0, omega1, 101, *seed)
	def __call__(self, t):
		return self.dx(t), self.dy(t)


class Tenant:
	color = 0, 80, 40
	def __init__(self, pP):
		self.pP = pP
		self.targetP = None
		self.alive = True
		self.t = 0
		self.seed = random.random()
		self.point = 0
		self.flip = False
		self.flail = Lissajous(0.2, 2, 3, self.seed)
		self.color = random.choice([
			(240, 160, 160),
			(240, 200, 160),
			(240, 240, 160),
			(160, 240, 160),
			(120, 240, 240),
			(160, 160, 240),
		])
		self.imgname = "fish-0"

	def think(self, dt):
		self.t += dt
		self.point = math.softapproach(self.point, 0, 1 * dt)
		v = 4
		if self.targetP is not None:
			self.pP = math.softapproach(self.pP, self.targetP, v * dt, dymin = 0.01)
			if self.pP == self.targetP:
				self.targetP = None
		if self.targetP is None and 0.1 * random.random() < dt:
			self.settarget(self.selecttarget())
		if 0.4 * random.random() < dt:
			effects.addbreathbubbleP(self.pP)

	def settarget(self, targetP):
		self.targetP = targetP
		if self.targetP is not None and self.targetP != self.pP:
			dxP, dyP = math.vminus(self.targetP, self.pP)
			self.point = math.degrees(math.atan2(dyP, abs(dxP))) * (1 if dxP > 0 else -1)
			self.flip = dxP < 0

	def selecttarget(self):
		if not self.alive: return None
		structures = grid.grid.structures
		if not structures: return None
		structure = random.choice(structures)
		pG = random.choice(structure.ps)
		return view.PconvertG(pG)

	def draw(self):
		pP = math.vtplus(self.pP, self.flail(self.t))
		angle = self.point + 10 * math.sin(2 * self.t)
		color = self.color
		graphics.drawimgP(pP, self.imgname, scaleP = 0.3, angle = angle, flip_x = self.flip, color = color)


class Shopper(Tenant):
	color = 200, 100, 100
	amount = 5
	def __init__(self, home, inert):
		Tenant.__init__(self, view.PconvertG(home.p0))
		self.home = home
		self.inert = inert
		self.destination = None
		self.arrived = False
		self.targetP = view.PconvertG(self.home.pbase)
		self.pop = not self.inert

	def forcehome(self, pG):
		self.pP = view.PconvertG(pG)
		self.targetP = None
		self.destination = None
		self.arrived = False

	def think(self, dt):
		Tenant.think(self, dt)
		if self.destination is not None and not self.destination.alive:
			pG = view.GnearestP(self.pP)
			if pG in self.destination.ps:
				pG = self.destination.pbase
			elif pG not in grid.grid.nodes:
				pG = 0, 0
			self.forcehome(pG)

	def arrive(self):
		self.arrived = True
		self.destination.arrive(self)

	def fulfill(self):
		effects.addinfoP(self.pP, f"+${self.amount}")
		state.earn(self.amount)
		self.settargetG(self.destination.pbase)
		self.destination = None
		self.arrived = False
		sound.play("buy")

	def settargetG(self, targetG):
		self.settarget(view.PconvertG(targetG))

	def selecttarget(self):
		targetG = self.selecttargetG()
		return view.PconvertG(targetG) if targetG is not None else None

	def selecttargetG(self):
		pG = view.GnearestP(self.pP)
		if not self.inert and pG not in grid.grid.nodes:
			self.pP = 0, 0
			return None
		def randomp(ps):
			return random.choice(list(grid.adjsof(pG, ps)))
		if self.arrived:
			return randomp(self.destination.ps)
		if self.destination is None:
			if pG in self.home.ps:
				if not self.inert and random.random() < 1 and self.home.nearestshop():
					self.destination = self.home.nearestshop()
					return self.selecttargetG()
				else:
					return randomp(self.home.ps)
			elif pG == self.home.pbase:
				return randomp(self.home.ps)
			else:
				return grid.stepto(pG, self.home.pbase)
		else:
			if pG in self.destination.ps:
				self.arrive()
				return self.selecttargetG()
			elif pG == self.destination.pbase:
				return randomp(self.destination.ps)
			else:
				return grid.stepto(pG, self.destination.pbase)
			
class Vendor:
	color = 160, 60, 140
	def __init__(self, home, inert):
		self.home = home
		self.inert = inert
		self.pP = view.PconvertG(home.p0)
		self.alive = True
		self.t = 0
		self.seed = random.random()
		self.flail = Lissajous(0.1, 2, 3, 200, self.seed)
		self.rock = Oscillator(10, 2, 3, 201, self.seed)
		self.puff = Oscillator(0.1, 2, 3, 202, self.seed)
		self.imgname = "puff-0"
		self.pop = False
		self.scaleP = 0.4 * (6 / self.home.Tstock) ** 0.3

	def drawp(self):
		return math.vtplus(self.pP, self.flail(self.t))


	def think(self, dt):
		self.t += dt
		if 0.4 * random.random() < dt:
			effects.addbreathbubbleP(math.vtplus(self.drawp(), (0, 1), 0.4))

	def draw(self):
		scaleP = self.scaleP * math.exp(self.puff(self.t))
		if not self.inert:
			scaleP *= math.mix(0.6, 1, self.home.fstock)
		angle = self.rock(self.t)
		text = "" if self.inert else f"{int(self.home.fstock * 100)}%"
		graphics.drawimgtextP(self.drawp(), self.imgname, text, scaleP = scaleP, angle = angle, color = self.color)



