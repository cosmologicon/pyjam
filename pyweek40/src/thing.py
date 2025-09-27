import pygame, math, random
from . import view, grid, pview, effects, state, fuzz, graphics
from .pview import T

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
		self.omega0 = fuzz.uniform(2, 3, 0, self.seed)
		self.omega1 = fuzz.uniform(2, 3, 1, self.seed)
		self.phi0 = fuzz.uniform(0, math.tau, 2, self.seed)
		self.phi1 = fuzz.uniform(0, math.tau, 3, self.seed)

	def think(self, dt):
		self.t += dt
		self.point = math.softapproach(self.point, 0, 1 * dt)
		v = 4
		if self.targetP is not None:
			self.pP = math.softapproach(self.pP, self.targetP, v * dt, dymin = 0.01)
			if self.pP == self.targetP:
				self.targetP = None
		if self.targetP is None: # and random.random() < dt:
			self.settarget(self.selecttarget())

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

	def offsetP(self):
		dxP = 0.2 * math.sin(self.omega0 * self.t + self.phi0)
		dyP = 0.2 * math.sin(self.omega1 * self.t + self.phi1)
		return dxP, dyP

	def draw(self):
		pP = math.vtplus(self.pP, self.offsetP())
		angle = self.point + 10 * math.sin(2 * self.t)
		graphics.drawimgP(pP, "fish", scaleP = 0.3, angle = angle, flip_x = self.flip, color = self.color)


class Shopper(Tenant):
	color = 200, 100, 100
	amount = 10
	def __init__(self, home):
		Tenant.__init__(self, view.PconvertG(home.p0))
		self.home = home
		self.destination = None
		self.arrived = False
		self.targetP = view.PconvertG(self.home.pbase)

	def arrive(self):
		self.arrived = True
		self.destination.arrive(self)

	def fulfill(self):
		effects.addinfoP(self.pP, f"+${self.amount}")
		state.earn(self.amount)
		self.settargetG(self.destination.pbase)
		self.destination = None
		self.arrived = False

	def settargetG(self, targetG):
		self.settarget(view.PconvertG(targetG))

	def selecttarget(self):
		targetG = self.selecttargetG()
		return view.PconvertG(targetG) if targetG is not None else None

	def selecttargetG(self):
		pG = view.GnearestP(self.pP)
		def randomp(ps):
			return random.choice(list(grid.adjsof(pG, ps)))
		if self.arrived:
			return randomp(self.destination.ps)
		if self.destination is None:
			if pG in self.home.ps:
				if random.random() < 1 and self.home.nearestshop():
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
			



