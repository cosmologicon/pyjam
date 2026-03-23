import pygame, math
from . import view, control, world
from . import fuzz, pview, ptext
from .pview import T

def shrinkline(p0, p1, dpmax, fmin = 0.1):
	d = math.distance(p0, p1)
	f = min(dpmax / d, fmin)
	return math.mix(p0, p1, f), math.mix(p0, p1, 1 - f)
	
	

class Star:
	def __init__(self, pos, mag):
		self.pos = pos
		self.mag = mag
		self.links = []
		self.N = fuzz.choice([1, 2, 3, 4], 0.567, *pos)

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

	def draw(self):
		pV = view.VconvertG(self.pos)
		rV = pview.T(5) if self is control.cursor else pview.T(2)
		color = (255, 255, 255) if self is control.cursor else (200, 200, 200)
		pygame.draw.circle(pview.screen, color, pV, rV)
		color = (128, 128, 128) if self.N == len(self.links) else (255, 200, 200)
		ptext.draw(f"{self.N}", midbottom = pV, fontsize = T(20), color=color, owidth=1)
		

class Link:
	def __init__(self, star0, star1):
		self.star0 = star0
		self.star1 = star1
		self.stars = [self.star0, self.star1]

	def place(self):
		world.links.append(self)
		self.star0.addlink(self)
		self.star1.addlink(self)

	def unplace(self):
		world.links.remove(self)
		self.star0.removelink(self)
		self.star1.removelink(self)
	
	def draw(self):
		p0, p1 = shrinkline(self.star0.pos, self.star1.pos, 0.3)
		color = 80, 80, 160
		pygame.draw.aaline(pview.screen, color, view.VconvertG(p0), view.VconvertG(p1), 1)

