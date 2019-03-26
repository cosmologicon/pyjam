from __future__ import division
import pygame, math
from . import pview, ptext
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


# m = tan(60deg) = sqrt(3)
# A = 1/(1+m^2) [1-m^2, 2m, 2m, m^2 - 1] = 1/4 [-2, 2sqrt(3), 2sqrt(3), 2]
def R1(pos):
	x, y = pos
	m = math.sqrt(3)
	return (-x + m * y) / 2, (m * x + y) / 2
	
R2 = math.R(math.radians(-60))

def dim(color):
	return ptext._applyshade(color, 0.2)

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
		self.spec = spec
		self.img = None
		self.s = 1000

	@staticmethod
	def empty():
		spec = {
			"shapes": [],
		}
		return Design(spec)

	def colorat(self, pos):
		px, py = pos
		px = abs(px)
		py = abs(py)
		if py < 1 / math.sqrt(3) * px:
			px, py = math.R(math.radians(60), (px, py))
		elif py < math.sqrt(3) * px:
			px, py = R1((px, py))
		for shape in reversed(self.spec["shapes"]):
			if shapecontains(shape, (px, py)):
				return shape["color"]
		return None

	def makeimg(self):
		if self.img is not None:
			return self.img
		imgs = [pygame.Surface((self.s, self.s)).convert_alpha() for _ in range(3)]
		for img in imgs:
			img.fill((0, 0, 0, 0))
		for shape in self.spec["shapes"]:
			color = pygame.Color(shape["color"])
			sx, sy = shape["pos"]
			if shape["type"] == "circle":
				r = shape["r"]
				color = pygame.Color(color)
				sx1, sy1 = R1((sx, sy))
				sx2, sy2 = R2((sx, sy))
				pygame.draw.circle(imgs[0], color, I(sx * self.s, (1 - sy) * self.s), I(r * self.s))
				pygame.draw.circle(imgs[1], color, I(sx1 * self.s, (1 - sy1) * self.s), I(r * self.s))
				pygame.draw.circle(imgs[2], color, I(sx2 * self.s, (1 - sy2) * self.s), I(r * self.s))
			if shape["type"] == "shard":
				sw, sh = shape["size"]
				color0 = color
				color1 = dim(color0)
				for f, color in [(1, color1), (0.6, color0)]:
					S, C = math.norm((sx, sy), f)
					ps0 = [
						(sx + S * sh, sy + C * sh),
						(sx + C * sw, sy - S * sw),
						(sx - S * sh, sy - C * sh),
						(sx - C * sw, sy + S * sw),
					]
					ps1 = [R1(p) for p in ps0]
					ps2 = [R2(p) for p in ps0]
					pygame.draw.polygon(imgs[0], color, I([(x * self.s, (1 - y) * self.s) for x, y in ps0]))
					pygame.draw.polygon(imgs[1], color, I([(x * self.s, (1 - y) * self.s) for x, y in ps1]))
					pygame.draw.polygon(imgs[2], color, I([(x * self.s, (1 - y) * self.s) for x, y in ps2]))
			if shape["type"] == "blade":
				w = shape["width"]
				color0 = color
				color1 = dim(dim(color0))
				for (a, color) in [(w, color1), (w / 2, color0)]:
					S, C = math.norm((sx, sy), a)
					ps0 = [
						(-C, S),
						(C, -S),
						(sx + C, sy - S),
						(sx + 4 * S, sy + 4 * C),
						(sx - C, sy + S),
					]
					ps1 = [R1(p) for p in ps0]
					ps2 = [R2(p) for p in ps0]
					pygame.draw.polygon(imgs[0], color, I([(x * self.s, (1 - y) * self.s) for x, y in ps0]))
					pygame.draw.polygon(imgs[1], color, I([(x * self.s, (1 - y) * self.s) for x, y in ps1]))
					pygame.draw.polygon(imgs[2], color, I([(x * self.s, (1 - y) * self.s) for x, y in ps2]))

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

	def drawoverlay(self, pos, r):
		self.makeimg()
		img = pygame.transform.smoothscale(self.img, T(2 * r, 2 * r))
		img.blit(overlayalpha(r), (0, 0), None, pygame.BLEND_RGBA_MULT)
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

	def addshape(self, shapetype, pos, color, **kwargs):
		shape = {
			"type": shapetype,
			"pos": pos,
			"color": color,
		}
		shape.update(kwargs)
		self.spec["shapes"].append(shape)
		self.img = None

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


