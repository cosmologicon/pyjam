from __future__ import division
import pygame, math, numpy
from . import pview, ptext, render, shape, view
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
		p0, a0 = sliceimg(s, 0)
		p2, a2 = sliceimg(s, 2)
		p1 = pygame.surfarray.pixels3d(img)
		p1 -= p0
		p1 -= p2
		a1 = pygame.surfarray.pixels_alpha(img)
		a1 -= a0
		a1 -= a2
	if sector == 2:
		img.fill((0, 0, 0, 0))
		ps = [(0, s), (s, s), (s, s - a)]
		pygame.draw.polygon(img, (255, 255, 255, 255), ps)
	sliceimgcache[key] = pygame.surfarray.array3d(img) // 255, pygame.surfarray.array_alpha(img) // 255
	return sliceimgcache[key]

oalphacache = {}
def overlayalpha(s):
	key = s
	if key in oalphacache:
		return oalphacache[key]
	oimg = pygame.Surface((s, s)).convert_alpha()
	oimg.fill((255, 255, 255, 60))
	oimg.blit(sliceimg(s, 0), (0, 0), None, pygame.BLEND_RGBA_MULT)
	img = pygame.Surface((2 * s, 2 * s)).convert_alpha()
	img.fill((255, 255, 255, 60))
	img.blit(oimg, (s, 0), None, pygame.BLEND_RGBA_ADD)
	oalphacache[key] = img
	return img

def shapecontains(shape, pos):
	sx, sy = shape["pos"]
	theta = math.atan2(sx, sy) if sx or sy else 0
	dx, dy = math.R(theta, pos)
	dy -= math.length((sx, sy))
	if shape["type"] == "circle":
		return math.length(dx, dy) <= shape["r"]
	if shape["type"] == "shard":
		sw, sh = shape["size"]
		return abs(dx / sw) + abs(dy / sh) < 1
	if shape["type"] == "blade":
		w = shape["width"]
		dx = abs(dx / w)
		dy /= 4 * w
		return (dy < 0 and dx < 1) or (dy >= 0 and dx + dy < 1)

class Design:
	def __init__(self, spec):
		self.shapes = [shape.fromspec(s) for s in spec["shapes"]]
		self.img = None
		self.drawn = False
		self.s = 700

		self.sscale = None
		self.s0scale = None

	@staticmethod
	def empty():
		spec = {
			"shapes": [],
		}
		return Design(spec)

	def getspec(self):
		spec = {
			"shapes": [shape.getspec() for shape in self.shapes],
		}
		return spec

	def anchors(self):
		for i, shape in enumerate(self.shapes):
			for j, anchor in enumerate(shape.anchors):
				yield i, j, anchor

	def undraw(self):
		self.drawn = False
		self.sscale = None
		self.s0scale = None

	def colorat(self, pos):
		px, py = pos
		px = abs(px)
		py = abs(py)
		if py < 1 / math.sqrt(3) * px:
			px, py = math.R(math.radians(60), (px, py))
		elif py < math.sqrt(3) * px:
			px, py = render.R1((px, py))
		for shape in reversed(self.shapes):
			shapecolor = shape.colorat((px, py))
			if shapecolor is not None:
				return shapecolor
		return None

	def makeimg(self):
		if self.drawn:
			return self.img
		t0 = pygame.time.get_ticks()
		if self.img is None or self.img.get_width() != 2 * self.s:
			self.simgs = [pygame.Surface((self.s, self.s)).convert_alpha() for _ in range(3)]
			self.qimg = pygame.Surface((self.s, self.s)).convert_alpha()
			self.qpixels = pygame.surfarray.pixels3d(self.qimg)
			self.qalphas = pygame.surfarray.pixels_alpha(self.qimg)
			self.img = pygame.Surface((2 * self.s, 2 * self.s)).convert_alpha()
		for img in self.simgs:
			img.fill((0, 0, 0, 0))

		for shape in self.shapes:
			shape.sectordraw(self.simgs)

		# For some reason making these standalone arrays makes this worse?
		pixels, alphas = zip(*[sliceimg(self.s, j) for j in (0, 1, 2)])
		t1 = pygame.time.get_ticks()
		for j, simg in enumerate(self.simgs):
			mpixels, malphas = sliceimg(self.s, j)
			spixels = pygame.surfarray.pixels3d(simg)
			salphas = pygame.surfarray.pixels_alpha(simg)
			if j == 0:
				spixels[:,:,:] *= mpixels
				salphas[:,:] *= malphas
				self.qpixels[:,:,:] = spixels
				self.qalphas[:,:] = salphas
			else:
				self.qpixels += spixels * mpixels
				self.qalphas += salphas * malphas
		t2 = pygame.time.get_ticks()
		arr = numpy.concatenate([numpy.flip(self.qpixels, 0), self.qpixels], 0)
		arr = numpy.concatenate([arr, numpy.flip(arr, 1)], 1)
		pygame.surfarray.pixels3d(self.img)[:,:,:] = arr
		arr = numpy.concatenate([numpy.flip(self.qalphas, 0), self.qalphas], 0)
		arr = numpy.concatenate([arr, numpy.flip(arr, 1)], 1)
		pygame.surfarray.pixels_alpha(self.img)[:,:] = arr
		self.drawn = True
#		print(pygame.time.get_ticks() - t0, pygame.time.get_ticks() - t1, pygame.time.get_ticks() - t2)

	def getimgscale(self, r):
		key = r, pview.height
		if self.sscale == key:
			return self.imgscale
		self.makeimg()
		self.sscale = key
		if T(2 * r) == self.img.get_width():
			self.imgscale = self.img
		else:
			self.imgscale = pygame.transform.smoothscale(self.img, T(2 * r, 2 * r))
		return self.imgscale

	def getimg0scale(self, r):
		key = r, pview.height
		if self.s0scale == key:
			return self.img0scale
		self.makeimg()
		self.s0scale = key
		self.img0scale = pygame.transform.smoothscale(self.simgs[0], T(r, r))
		return self.img0scale

	def draw(self, Fspot):
		if not view.Fspotvisible(Fspot):
			return
		(x, y), r = Fspot
		img = self.getimgscale(r)
		pview.screen.blit(img, T(x - r, y - r))

	def drawoverlay(self, pos, r):
		self.makeimg()
		img = pygame.transform.smoothscale(self.img, T(2 * r, 2 * r))
		img.blit(overlayalpha(r), (0, 0), None, pygame.BLEND_RGBA_MULT)
		x, y = pos
		pview.screen.blit(img, T(x - r, y - r))

	def drawwedge(self, Fspot):
		(x, y), r = Fspot
		self.makeimg()
		img = self.getimg0scale(r)
		pview.screen.blit(img, T(x, y - r))

	def addcircle(self, pos, r, color):
		self.addshape("circle", pos, color, r=r)

	def addshard(self, pos, size, color):
		self.addshape("shard", pos, color, size=size)

class Flake:
	def __init__(self, spec, pos, r):
		self.design = spec if isinstance(spec, Design) else Design(spec)
		self.pos = pos
		self.r = r
	
	def draw(self):
		self.design.draw(self.pos, self.r)


