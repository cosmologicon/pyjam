import pygame, math, random
from . import view, grid, pview, effects, state
from .pview import T

class Tenant:
	color = 0, 80, 40
	def __init__(self, pP):
		self.pP = pP
		self.targetP = None
		self.home = None
		self.alive = True

	def think(self, dt):
		v = 4
		if self.targetP is not None:
			self.pP = math.approach(self.pP, self.targetP, v * dt)
			if self.pP == self.targetP:
				self.targetP = None
		if self.targetP is None and random.random() < dt:
			self.targetP = self.selecttarget()

	def selecttarget(self):
		if not self.alive: return None
		structures = grid.grid.structures
		if not structures: return None
		structure = random.choice(structures)
		pG = random.choice(structure.ps)
		return view.PconvertG(pG)
	
	def draw(self):
		pV = view.VconvertP(self.pP)
		rV = view.VscaleP(0.1)
		pygame.draw.circle(pview.screen, self.color, pV, rV)

class Shopper(Tenant):
	color = 200, 100, 100
	amount = 10
	def __init__(self, spawner, destination):
		Tenant.__init__(self, view.PconvertG(spawner.p0))
		self.destination = destination
		self.targetP = view.PconvertG(spawner.pbase)

	def arrive(self):
		if not self.alive: return
		self.alive = False
		effects.addinfoP(self.pP, f"+${self.amount}")
		state.earn(self.amount)
		

	def selecttarget(self):
		pG = view.GnearestP(self.pP)
		if self.pP == view.PconvertG(self.destination.p0):
			self.arrive()
			return None
		elif pG == self.destination.pbase:
			return view.PconvertG(self.destination.p0)
		else:
			return view.PconvertG(grid.stepto(pG, self.destination.pbase))
			



