import pygame, math, random, itertools
from . import view, control, world, graphics, effect, geometry, settings
from . import fuzz, pview, ptext
from .pview import T

class Star:
	colorset = [
		(255, 255, 255),
		(220, 220, 255),
		(180, 230, 255),
	]
	noadj = False
	islone = False
	def __init__(self, pos, mag, N):
		self.pos = pos
		self.mag = mag
		self.links = []
		self.N = N
		self.chimed = False
		self.label = f"{self.N}"
		self.conok = True
		self.color = fuzz.choice(self.colorset, 432, *pos)

	def ok(self):
		if not all(link.ok() for link in self.links):
			return self.setchimed(False)
		if self.N != len(self.links):
			return self.setchimed(False)
		return self.setchimed(True)

	def setchimed(self, chimed):
		if chimed and not self.chimed:
			effect.Chime(self.pos, self.label, self.color)
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
		return 0.3 * math.interp(self.mag, 0, 3, 6, 1)
		return 0.3 * math.interp(self.mag, 0, 1.4, 6, 1)
		return 0.2 * math.interp(self.mag, 0, 3, 6, 1)

	def draw(self):
		pV0 = view.VconvertG(self.pos)
		pV = math.CS(random.uniform(0, math.tau), r = random.uniform(0, 0.6), center = pV0)
		pV = pV0
		rV = view.VsmoothscaleG(self.rG())
		graphics.drawstarV(pV, rV, self.color)
		hcolor = (120, 120, 120) if self.ok() else (255, 255, 255)
		color = math.mixI(self.color, hcolor, 0.5)
		pVtext = view.VconvertG(geometry.vplus(self.pos, (0, 0.3)))
		alpha = math.interp(math.distance(self.pos, control.mouseG), 0, 1, 10, 0)
		if not self.ok():
			alpha = 1
		fontsize = T(32 if self is control.cursor else 20)
		ptext.draw(self.label, midbottom = pVtext, fontsize = fontsize, color=color, owidth=1, alpha=alpha)
		if settings.editor and self.mag < world.sky - world.dadvance:
			
			pygame.draw.circle(pview.screen, (255, 200, 100), pV0, view.VscaleG(self.rG() * 2), 1)

class LoneStar(Star):
	colorset = [(255, 180, 180)]
	islone = True
	def __init__(self, pos, mag, N):
		Star.__init__(self, pos, mag, N)
		assert self.N == 4
		self.label = "X"

	def ok(self):
		if not self.conok:
			return self.setchimed(False)
		return Star.ok(self)

	def draw(self):
		Star.draw(self)
		if self.conok:
			return False
		for dt in (0, 1/3, 2/3):
			t = (pygame.time.get_ticks() * 0.001 * 1 + dt) % 1
			d = 2 * t ** 0.5
			color = math.interpI(t, 0, (255, 100, 100), 1, (0, 0, 0))
			pygame.draw.circle(pview.screen, color, view.VconvertG(self.pos), view.VscaleG(d), 1)
		

class BalancedStar(Star):
	colorset = [(255, 255, 130)]
	def __init__(self, pos, mag, N):
		Star.__init__(self, pos, mag, N)
		self.balanced = True
		self.badpairs = []
		self.maxcos = math.cos(math.tau / (N + 1))
		assert self.N == 3
		self.label = "Y"

	def ok(self):
		if not self.balanced:
			return self.setchimed(False)
		return Star.ok(self)

	def unbalancedlinkpairs(self):
		pairs = []
		dps = [math.norm(geometry.vminus(star.pos, self.pos)) for star in self.adjs]
		for dp0, dp1 in itertools.combinations(dps, 2):
			if math.dot(dp0, dp1) > self.maxcos:
				yield dp0, dp1

	def setbalanced(self):
		self.badpairs = list(self.unbalancedlinkpairs())
		self.balanced = not self.badpairs
		

	def addlink(self, link):
		Star.addlink(self, link)
		self.setbalanced()
	
	def removelink(self, link):
		Star.removelink(self, link)
		self.setbalanced()

	def draw(self):
		Star.draw(self)
		for dp0, dp1 in self.badpairs:
			for dt in (0, 1/3, 2/3):
				t = (pygame.time.get_ticks() * 0.001 * 2 + dt) % 1
				d = 3 * t ** 0.5
				p0 = geometry.vplus(self.pos, dp0, d)
				p1 = geometry.vplus(self.pos, dp1, d)
				color = math.interpI(t, 0, (255, 100, 100), 1, (0, 0, 0))
				pygame.draw.aaline(pview.screen, color, view.VconvertG(p0), view.VconvertG(p1), 1)
			

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

	def shrinkline(self):
		return geometry.shrinkline(self.star0.pos, self.star1.pos, 1.5 * self.star0.rG(), 1.5 * self.star1.rG())

	def place(self):
		self.setcrossers()
		world.links.append(self)
		self.star0.addlink(self)
		self.star1.addlink(self)
		for crosser in self.crossers:
			crosser.crossers.append(self)
		if self.ok():
			effect.Strum(*self.shrinkline())
		world.resolvecon()
		world.save()

	def cross(self, link):
		return geometry.linecross(self.ps, link.ps)

	def unplace(self, resolve = True):
		world.links.remove(self)
		self.star0.removelink(self)
		self.star1.removelink(self)
		for crosser in self.crossers:
			crosser.crossers.remove(self)
		if resolve:
			world.resolvecon()
			world.setscore()
		graphics.dellinkimg()
		world.save()
	
	def draw(self):
		p0, p1 = self.shrinkline()
		color = (40, 40, 80) if self.ok() else (160, 80, 80)
		graphics.drawlinkV(view.VconvertG(p0), view.VconvertG(p1), view.VscaleG(0.06), color)
#		pygame.draw.aaline(pview.screen, color, view.VconvertG(p0), view.VconvertG(p1), 1)

# Pseudo-star used by the control module while dragging.
class CursorStar:
	noadj = False
	def __init__(self, pos):
		self.pos = pos

class CursorLink(Link):
	def __init__(self, star0, cursor):
		Link.__init__(self, star0, cursor)
		self.setcrossers()

	def draw(self):
		rG = 1.5 * self.star0.rG()
		if math.distance(self.star0.pos, self.star1.pos) < rG:
			return
		p0, p1 = geometry.shrinkline(self.star0.pos, self.star1.pos, rG, 0)
		color = (40, 40, 80) if self.ok() else (160, 80, 80)
		color = math.mixI(color, (255, 255, 255), 0.6)
		pygame.draw.aaline(pview.screen, color, view.VconvertG(p0), view.VconvertG(p1), 1)
		if math.distance(self.star0.pos, self.star1.pos) > rG:
			pygame.draw.circle(pview.screen, color, view.VconvertG(self.star0.pos), view.VscaleG(rG), 1)




