import math, pygame
from . import view, pview, world, geometry

class Effect:
	T = 1
	def __init__(self):
		self.t = 0
		self.f = 0
		world.effects.append(self)
	def think(self, dt):
		self.t += dt
		self.f = math.interp(self.t, 0, 0, self.T, 1)
		self.alive = self.t <= self.T

class Chime(Effect):
	T = 0.5
	def __init__(self, pos):
		Effect.__init__(self)
		self.pos = pos
	def think(self, dt):
		Effect.think(self, dt)
	def draw(self):
		pV = view.VconvertG(self.pos)
		rG = math.mix(0.5, 2, self.f ** 0.5)
		rV = view.VscaleG(rG)
		color = 50, 50, 200
		pygame.draw.circle(pview.screen, color, pV, rV, 1)

class Strum(Effect):
	T = 0.5
	def __init__(self, pos0, pos1):
		Effect.__init__(self)
		self.pos0 = pos0
		self.pos1 = pos1
		self.ps = [pos0, pos1]
		dx, dy = math.norm(geometry.vminus(pos1, pos0))
		self.dpos = -dy, dx
	def think(self, dt):
		Effect.think(self, dt)
	def draw(self):
		r = math.mix(0, 0.6, self.f ** 0.5)
		color = 50, 50, 200
		for a in (-1, 1):
			pGs = [geometry.vplus(p, self.dpos, a * r) for p in self.ps]
			pVs = [view.VconvertG(pG) for pG in pGs]
			pygame.draw.aaline(pview.screen, color, *pVs, 1)

