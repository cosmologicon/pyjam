import pygame, math, random
from . import view, control, world, graphics, effect, geometry
from . import fuzz, pview, ptext
from .pview import T

class Star:
	def __init__(self, pos, mag):
		self.pos = pos
		self.mag = mag
		self.links = []
		self.N = fuzz.choice([1, 2, 3, 4], 0.567, *pos)
		self.chimed = False

	def ok(self):
		if not all(link.ok() for link in self.links):
			self.chimed = False
			return False
		if self.N != len(self.links):
			self.chimed = False
			return False
		if not self.chimed:
			self.chimed = True
			effect.Chime(self.pos)
		self.chimed = True
		return True


	def distanceto(self, pG):
		return math.distance(self.pos, pG)

	def addlink(self, link):
		self.links.append(link)
	
	def removelink(self, link):
		self.links.remove(link)

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
		color = (255, 255, 255)
		color = math.interpI(random.uniform(0, 0.2), 0, color, 1, (0, 0, 0))
		graphics.drawstarV(pV, rV, color)
		color = (120, 120, 120) if self.ok() else (200, 255, 200)
		pVtext = view.VconvertG(geometry.vplus(self.pos, (0, 0.3)))
		alpha = math.interp(math.distance(self.pos, control.mouseG), 0, 1, 15, 0)
		if not self.ok():
			alpha = 1
		ptext.draw(f"{self.N}", midbottom = pVtext, fontsize = T(20), color=color, owidth=1, alpha=alpha)

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

	def ok(self):
		return not self.crossers

	def setcrossers(self):
		self.crossers = [link for link in world.links if self.cross(link)]

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

