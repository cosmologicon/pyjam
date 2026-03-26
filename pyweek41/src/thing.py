import pygame, math, random, itertools
from . import view, control, world, graphics, effect, geometry
from . import fuzz, pview, ptext
from .pview import T

class Star:
	color = 255, 255, 255
	noadj = False
	def __init__(self, pos, mag, N):
		self.pos = pos
		self.mag = mag
		self.links = []
		self.N = N
		self.chimed = False

	def ok(self):
		if not all(link.ok() for link in self.links):
			return self.setchimed(False)
		if self.N != len(self.links):
			return self.setchimed(False)
		return self.setchimed(True)

	def setchimed(self, chimed):
		if chimed and not self.chimed:
			effect.Chime(self.pos)
		self.chimed = chimed
		return self.chimed

	def distanceto(self, pG):
		return math.distance(self.pos, pG)

	def addlink(self, link):
		self.links.append(link)
		self.adjs = [link.other(self) for link in self.links]
	
	def removelink(self, link):
		self.links.remove(link)
		self.adjs = [link.other(self) for link in self.links]

	def haslinkto(self, star):
		for link in self.links:
			if star in link.stars:
				return link
		return None

	def rG(self):
		return 0.2 * math.interp(self.mag, 0, 3, 6, 1)

	def draw(self):
		pV0 = view.VconvertG(self.pos)
		pV = math.CS(random.uniform(0, math.tau), r = random.uniform(0, 0.6), center = pV0)
		pV = pV0
		rV = view.VsmoothscaleG(self.rG() * (2 if self is control.cursor else 1))
		color = math.interpI(random.uniform(0, 0.2), 0, self.color, 1, (0, 0, 0))
		graphics.drawstarV(pV, rV, color)
		color = (120, 120, 120) if self.ok() else (200, 255, 200)
		pVtext = view.VconvertG(geometry.vplus(self.pos, (0, 0.3)))
		alpha = math.interp(math.distance(self.pos, control.mouseG), 0, 1, 15, 0)
		if not self.ok():
			alpha = 1
		ptext.draw(f"{self.N}", midbottom = pVtext, fontsize = T(20), color=color, owidth=1, alpha=alpha)

class NoadjStar(Star):
	color = 255, 100, 100
	noadj = True

class BalancedStar(Star):
	color = 100, 255, 100
	def __init__(self, pos, mag, N):
		Star.__init__(self, pos, mag, N)
		self.balanced = True
		self.maxcos = math.cos(math.tau / (N + 1))

	def ok(self):
		if not self.balanced:
			return self.setchimed(False)
		return Star.ok(self)

	def setbalanced(self):
		self.balanced = True
		dps = [math.norm(geometry.vminus(star.pos, self.pos)) for star in self.adjs]
		for dp0, dp1 in itertools.combinations(dps, 2):
			if math.dot(dp0, dp1) > self.maxcos:
				self.balanced = False
		

	def addlink(self, link):
		Star.addlink(self, link)
		self.setbalanced()
	
	def removelink(self, link):
		Star.removelink(self, link)
		self.setbalanced()

	
# Pseudo-star used by the control module while dragging.
class Cursor:
	def __init__(self, pos):
		self.pos = pos

class Link:
	def __init__(self, star0, star1):
		self.star0 = star0
		self.star1 = star1
		self.stars = [self.star0, self.star1]
		self.ps = [self.star0.pos, self.star1.pos]
		self.crossers = []
		self.badadj = self.star0.noadj and self.star1.noadj

	def ok(self):
		return not self.badadj and not self.crossers

	def setcrossers(self):
		self.crossers = [link for link in world.links if self.cross(link)]

	def other(self, star):
		if star is self.star0: return self.star1
		if star is self.star1: return self.star0
		return None

	def place(self):
		self.setcrossers()
		world.links.append(self)
		self.star0.addlink(self)
		self.star1.addlink(self)
		for crosser in self.crossers:
			crosser.crossers.append(self)
		if self.ok():
			effect.Strum(*self.ps)

	def cross(self, link):
		return geometry.linecross(self.ps, link.ps)

	def unplace(self):
		world.links.remove(self)
		self.star0.removelink(self)
		self.star1.removelink(self)
		for crosser in self.crossers:
			crosser.crossers.remove(self)
	
	def draw(self):
		p0, p1 = geometry.shrinkline(self.star0.pos, self.star1.pos, 1.5 * self.star0.rG(), 1.5 * self.star1.rG())
		color = (40, 40, 80) if self.ok() else (160, 80, 80)
		pygame.draw.aaline(pview.screen, color, view.VconvertG(p0), view.VconvertG(p1), 1)

