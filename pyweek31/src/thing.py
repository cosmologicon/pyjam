import math
import pygame
from . import enco, pview
from . import view, state

class WorldBound(enco.Component):
	def __init__(self):
		self.pG = 0, 0
		self.rG = 0.25
	def draw(self):
		pV = view.VconvertG(self.pG)
		rV = view.VscaleG(self.rG)
		pygame.draw.circle(pview.screen, self.color, pV, rV)

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
	def draw(self):
		dG = view.GconvertH(self.dH)
		p0V = view.VconvertG(self.pG)
		p1V = view.VconvertG(view.vecadd(self.pG, dG, 0.3))
		pygame.draw.line(pview.screen, self.color, p0V, p1V)
		


@WorldBound()
@Travels(1)
class Ant:
	color = 250, 150, 100
	def __init__(self, pH, dH):
		self.tile = pH
		self.dH = dH
		self.setnext()

@WorldBound()
class BugSpawner:
	color = 100, 100, 100


@WorldBound()
class Maple:
	color = 0, 0, 0
	def __init__(self, pH):
		self.pH = pH
		self.pG = view.GconvertH(self.pH)
	def direct(self, bug):
		assert bug.tile == self.pH
		dH = view.HrotH(bug.dH)
		tile = view.vecadd(self.pH, dH)
		return tile, dH

