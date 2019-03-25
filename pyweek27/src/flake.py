from __future__ import division
import pygame, math
from . import pview
from .pview import I, T


sliceimgcache = {}
def sliceimg(s, sector):
	key = s, sector
	if key in sliceimgcache:
		return sliceimgcache[key]
	a = int(round(s * math.tan(math.radians(30))))
	img = pygame.Surface((s, s)).convert_alpha()
	if sector == 0:
		img.fill((0, 0, 0, 0))
		ps = [(0, s), (0, 0), (a, 0)]
		pygame.draw.polygon(img, (255, 255, 255, 255), ps)
	if sector == 1:
		img.fill((255, 255, 255, 255))
		img.blit(sliceimg(s, 0), (0, 0), None, pygame.BLEND_RGBA_SUB)
		img.blit(sliceimg(s, 2), (0, 0), None, pygame.BLEND_RGBA_SUB)
	if sector == 2:
		img.fill((0, 0, 0, 0))
		ps = [(0, s), (s, s), (s, s - a)]
		pygame.draw.polygon(img, (255, 255, 255, 255), ps)
	sliceimgcache[key] = img
	return img


# m = tan(60deg) = sqrt(3)
# A = 1/(1+m^2) [1-m^2, 2m, 2m, m^2 - 1] = 1/4 [-2, 2sqrt(3), 2sqrt(3), 2]
def R1(pos):
	x, y = pos
	m = math.sqrt(3)
	return (-x + m * y) / 2, (m * x + y) / 2
	
R2 = math.R(math.radians(-60))

class Design:
	def __init__(self, spec):
		self.spec = spec
		self.img = None
		self.s = 1000

	@staticmethod
	def empty():
		spec = {
			"circles": [],
		}
		return Design(spec)

	def makeimg(self):
		if self.img is not None:
			return self.img
		imgs = [pygame.Surface((self.s, self.s)).convert_alpha() for _ in range(3)]
		for img in imgs:
			img.fill((0, 0, 0, 0))
		for (cx, cy), cr, color in self.spec["circles"]:
			cx1, cy1 = R1((cx, cy))
			cx2, cy2 = R2((cx, cy))
			color = pygame.Color(color)
			pygame.draw.circle(imgs[0], color, I(cx * self.s, (1 - cy) * self.s), I(cr * self.s))
			pygame.draw.circle(imgs[1], color, I(cx1 * self.s, (1 - cy1) * self.s), I(cr * self.s))
			pygame.draw.circle(imgs[2], color, I(cx2 * self.s, (1 - cy2) * self.s), I(cr * self.s))
		qimg = pygame.Surface((self.s, self.s)).convert_alpha()
		qimg.fill((0, 0, 0, 0))
		for sector, img in enumerate(imgs):
			img.blit(sliceimg(self.s, sector), (0, 0), None, pygame.BLEND_RGBA_MIN)
			qimg.blit(img, (0, 0))
		self.img = pygame.Surface((2 * self.s, 2 * self.s)).convert_alpha()
		self.img.fill((0, 0, 0, 0))
		self.img.blit(qimg, (self.s, 0))
		self.img.blit(pygame.transform.flip(qimg, True, False), (0, 0))
		self.img.blit(pygame.transform.flip(qimg, True, True), (0, self.s))
		self.img.blit(pygame.transform.flip(qimg, False, True), (self.s, self.s))
		self.img0 = imgs[0]

	def draw(self, pos, r):
		self.makeimg()
		img = pygame.transform.smoothscale(self.img, T(2 * r, 2 * r))
		x, y = pos
		pview.screen.blit(img, T(x - r, y - r))

	def drawwedge(self, pos, r):
		self.makeimg()
		img = pygame.transform.smoothscale(self.img0, T(r, r))
		x, y = pos
		pview.screen.blit(img, T(x, y - r))
		C, S = math.CS(math.radians(30))
		ps = T([(x, y - r), (x, y), (x + S * r, y - C * r)])
		pygame.draw.aalines(pview.screen, pygame.Color("white"), False, ps)

	def addcircle(self, pos, r, color):
		self.spec["circles"].append((pos, r, color))
		self.img = None

class Flake:
	def __init__(self, spec, pos, r):
		self.design = spec if isinstance(spec, Design) else Design(spec)
		self.pos = pos
		self.r = r
	
	def draw(self):
		self.design.draw(self.pos, self.r)


