import pygame, math, os
from collections import defaultdict
from functools import lru_cache
from . import view, pview, geometry, ptext

@lru_cache(10)
def sparesurf(name, size):
	return pygame.Surface(size).convert_alpha()


timings = defaultdict(int)

class Mask:
	maskheight = None
	def __init__(self):
		t0 = pygame.time.get_ticks()
		self.surf = sparesurf("msurf", pview.size)
		self.surf.fill((0, 0, 0, 0))
		if self.maskheight is None:
			self.mask = sparesurf("mask", pview.size)
		else:
			width = int(round(self.maskheight * pview.aspect))
			self.mask = sparesurf("mask", (width, self.maskheight))
		self.mask.fill((255, 255, 255, 0))
		timings["init"] += pygame.time.get_ticks() - t0
		
	def setmask(self, plook, Aset):
		t0 = pygame.time.get_ticks()
		for Ainterval in Aset.intervals:
			ps = [
				plook,
				math.CS(Ainterval.A0, 1000, plook),
				math.CS(Ainterval.A1, 1000, plook),
			]
			ps = [view.screenpos(p) for p in ps]
			if self.mask.get_height() != pview.height:
				f = self.mask.get_height() / pview.height
				ps = [pview.I(f * x, f * y) for x, y in ps]
			pygame.draw.polygon(self.mask, (255, 255, 255, 255), ps)
		timings["setmask"] += pygame.time.get_ticks() - t0

	def exclude(self, plook, poly, jwall = None):
		t0 = pygame.time.get_ticks()
		for kwall, (p1, p2) in enumerate(geometry.rotpoly(poly)):
			if jwall == kwall:
				continue
			q1 = geometry.vecadd(plook, math.norm(geometry.vecsub(p1, plook), 1000))
			q2 = geometry.vecadd(plook, math.norm(geometry.vecsub(p2, plook), 1000))
			ps = [p1, p2, q2, q1]
			ps = [view.screenpos(p) for p in ps]
			if self.mask.get_height() != pview.height:
				f = self.mask.get_height() / pview.height
				ps = [pview.I(f * x, f * y) for x, y in ps]
			pygame.draw.polygon(self.mask, (255, 255, 255, 0), ps)
		timings["exclude"] += pygame.time.get_ticks() - t0


	def draw(self):
		t0 = pygame.time.get_ticks()
		if self.mask.get_height() != pview.height:
			self.mask = pygame.transform.scale(self.mask, pview.size, sparesurf("mask", pview.size))
		self.surf.blit(self.mask, (0, 0), None, pygame.BLEND_RGBA_MIN)
		pview.screen.blit(self.surf, (0, 0))
		timings["draw"] += pygame.time.get_ticks() - t0


class LookerMask:
	maskheight = None
	def __init__(self):
		t0 = pygame.time.get_ticks()
		self.surf = sparesurf("msurf", pview.size)
		self.surf.fill((0, 0, 0, 0))
		if self.maskheight is None:
			self.mask = sparesurf("mask", pview.size)
		else:
			width = int(round(self.maskheight * pview.aspect))
			self.mask = sparesurf("mask", (width, self.maskheight))
		self.mask.fill((255, 255, 255, 255))
		timings["linit"] += pygame.time.get_ticks() - t0
		
	def setmask(self, plook, poly, jwall = None):
		t0 = pygame.time.get_ticks()
		for kwall, (p1, p2) in enumerate(geometry.rotpoly(poly)):
			if jwall == kwall:
				continue
			q1 = geometry.vecadd(plook, math.norm(geometry.vecsub(p1, plook), 1000))
			q2 = geometry.vecadd(plook, math.norm(geometry.vecsub(p2, plook), 1000))
			ps = [p1, p2, q2, q1]
			ps = [view.screenpos(p) for p in ps]
			if self.mask.get_height() != pview.height:
				f = self.mask.get_height() / pview.height
				ps = [pview.I(f * x, f * y) for x, y in ps]
			pygame.draw.polygon(self.mask, (128, 128, 128, 255), ps)
		timings["lsetmask"] += pygame.time.get_ticks() - t0

	def draw(self):
		t0 = pygame.time.get_ticks()
		if self.mask.get_height() != pview.height:
			self.mask = pygame.transform.scale(self.mask, pview.size, sparesurf("mask", pview.size))
		self.surf.blit(self.mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
		pview.screen.blit(self.surf, (0, 0))
		timings["ldraw"] += pygame.time.get_ticks() - t0



def getplateimg(s):
	img = pygame.Surface((160, 160)).convert_alpha()
	img.fill((0, 0, 0, 0))
	pygame.draw.circle(img, (50, 50, 50), (80, 80), 72)
	ptext.draw(s, color = "white", shadow = (1, 1), alpha = 0.2,
		fontsize = 90, center = (80, 80), fontname = "Lobster",
		surf=img)
	return img


@lru_cache(1000)
def loadimg(imgname):
	if imgname.startswith("plate-"):
		return getplateimg(imgname[6:][:-4])
	return pygame.image.load(os.path.join("img", imgname)).convert_alpha()

@lru_cache(1000)
def getimg0(imgname, angle, scale, flip = False):
	img = loadimg(f"{imgname}.png")
	if flip:
		img = pygame.transform.flip(img, True, False)
	return pygame.transform.rotozoom(img, angle, scale)

@lru_cache(1)
def backgroundimg(size):
	return pygame.transform.smoothscale(loadimg("starfield.jpg"), size)
	

Nrot = 24
Nscale = 20
def getimg(imgname, A, scale, flip = False):
	angle = int(round((math.degrees(A) / 360 * Nrot))) % Nrot * (360 / Nrot)
	scale = math.exp(int(round(math.log(scale) * Nscale)) / Nscale)
	return getimg0(imgname, angle, scale, flip)

def drawimg(imgname, pos, A, scale, flip = False, surf = None):
	surf = surf or pview.screen
	img = getimg(imgname, A, scale, flip)
	rect = img.get_rect(center = pos)
	surf.blit(img, rect)

def drawimgw(imgname, pos, A, scale = 1, flip = False, surf = None):
	drawimg(imgname, view.screenpos(pos), A, 0.001 * view.screenscale(1000 * scale), flip, surf)

