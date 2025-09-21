import pygame, math, random
from . import view, grid, pview
from .pview import T

class Tenant:
	color = 0, 80, 40
	def __init__(self, pP):
		self.pP = pP
		self.targetP = None
		self.home = None

	def think(self, dt):
		v = 4
		if self.targetP is not None:
			self.pP = math.approach(self.pP, self.targetP, v * dt)
			if self.pP == self.targetP:
				self.targetP = None
		if self.targetP is None and random.random() < dt:
			self.targetP = self.Prandomtarget()

	def Prandomtarget(self):
		structures = grid.grid.structures
		if not structures: return None
		structure = random.choice(structures)
		pG = random.choice(structure.ps)
		return view.PconvertG(pG)
	
	def draw(self):
		pV = view.VconvertP(self.pP)
		rV = view.VscaleP(0.1)
		pygame.draw.circle(pview.screen, self.color, pV, rV)





