import math, pygame
from . import view, pview, world, geometry, sound, graphics, ptext

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
	def __init__(self, pos, label, color):
		Effect.__init__(self)
		sound.playchime()
		self.pos = pos
		self.label = label
		self.color = color
	def think(self, dt):
		Effect.think(self, dt)
	def draw(self):
		pV = view.VconvertG(self.pos)
		fontsize = pview.T(math.mix(20, 100, self.f ** 0.2))
		alpha = math.mix(1, 0, self.f)
		ptext.draw(self.label, center = pV, color = self.color, alpha = alpha, fontsize = fontsize, owidth = 1)
		return


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
		sound.playstrum()
	def think(self, dt):
		Effect.think(self, dt)
	def draw(self):
		r = math.mix(0, 2, self.f ** 0.2)
		color = 50, 50, 200
		alpha = math.mix(0.1, 0, self.f)
		pVs = []
		for a, p in [(-1, self.pos0), (-1, self.pos1), (1, self.pos1), (1, self.pos0)]:
			pG = geometry.vplus(p, self.dpos, a * r)
			pVs.append(view.VconvertG(pG))
		graphics.drawstrum(pVs, color, alpha)

