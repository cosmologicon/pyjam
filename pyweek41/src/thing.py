import pygame, math, random
from . import view, control, world, graphics
from . import fuzz, pview, ptext
from .pview import T

def shrinkline(p0, p1, dp0, dp1, fmax = 0.3):
	d = math.distance(p0, p1)
	f0 = min(dp0 / d, fmax)
	f1 = min(dp1 / d, fmax)
	return math.mix(p0, p1, f0), math.mix(p0, p1, 1 - f1)

# https://www.reddit.com/r/algorithms/comments/9moad4/comment/e7gvsjv/
def cross(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	return x0 * y1 - x1 * y0
def vplus(p0, p1, f = 1):
	x0, y0 = p0
	x1, y1 = p1
	return x0 + x1 * f, y0 + y1 * f
def vminus(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	return x0 - x1, y0 - y1
def orient(p0, p1, p2):
	return cross(vminus(p1, p0), vminus(p2, p0))
# Does the line segment (pA, pB) cross the line segment (pC, pD)
def linecross(seg0, seg1):
	pA, pB = seg0
	pC, pD = seg1
	return orient(pC, pD, pA) * orient(pC, pD, pB) < 0 and orient(pA, pB, pC) * orient(pA, pB, pD) < 0


class Star:
	def __init__(self, pos, mag):
		self.pos = pos
		self.mag = mag
		self.links = []
		self.N = fuzz.choice([1, 2, 3, 4], 0.567, *pos)

	def ok(self):
		if not all(link.ok() for link in self.links): return False
		if self.N != len(self.links): return False
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
		color = (255, 255, 255) if self is control.cursor else (200, 200, 200)
		color = math.interpI(random.uniform(0, 0.2), 0, color, 1, (0, 0, 0))
		graphics.drawstarV(pV, rV, color)
		color = (120, 120, 120) if self.ok() else (200, 255, 200)
		pVtext = view.VconvertG(vplus(self.pos, (0, 0.3)))
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

	def cross(self, link):
		return linecross(self.ps, link.ps)

	def unplace(self):
		world.links.remove(self)
		self.star0.removelink(self)
		self.star1.removelink(self)
		for crosser in self.crossers:
			crosser.crossers.remove(self)
	
	def draw(self):
		p0, p1 = shrinkline(self.star0.pos, self.star1.pos, 1.5 * self.star0.rG(), 1.5 * self.star1.rG())
		color = (40, 40, 80) if self.ok() else (160, 80, 80)
		pygame.draw.aaline(pview.screen, color, view.VconvertG(p0), view.VconvertG(p1), 1)

