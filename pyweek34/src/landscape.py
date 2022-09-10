# Coordinate systems:
# positive x is to the right, positive y is down
# xG, yG: game coordinates
# xP, yP: grid coordinates (i.e. the numpy array itself)
# xS, yS: standard screen coordinates, i.e. coordinates at default resolution
# xV, yV: actual screen (viewport) coordinates

# VscaleS = pview.f
# VconvertS = pview.T


import pygame, numpy
from functools import lru_cache
from . import maff

cache = lru_cache(None)

@cache
def anchor(ix, iy, d):
	return maff.fuzzrange(-1, 1, ix, iy, d)
def level(x, y, d, wrap = 16):
	ix, fx = divmod(x, 1)
	iy, fy = divmod(y, 1)
	ix %= wrap
	iy %= wrap
	jx = (ix + 1) % wrap
	jy = (iy + 1) % wrap
	return maff.mix(
		maff.mix(anchor(ix, iy, d), anchor(jx, iy, d), fx),
		maff.mix(anchor(ix, jy, d), anchor(jx, jy, d), fx),
		fy)
def noise(x, y):
	S, C = 0.6 * 2, 0.8 * 2
	a = 0
	f = 1
	for d in range(6):
		a += f * level(x, y, d)
		x, y = C * x + S * y, -S * x + C * y
		f *= 0.7
	return a


class Hmap:
	def __init__(self, size):
		self.size = size
		self.surf = pygame.Surface(size).convert_alpha()
		self.ready = False
		self.progress = 0
		self.ocean = pygame.Surface(size).convert_alpha()
	def killtime(self):
		if self.ready:
			return
		w, h = self.size
		y = self.progress
		for x in range(w):
			m = noise(0.005 * x, 0.005 * y)
			c = int(maff.interp(m, -2, 50, 2, 150))
			self.surf.set_at((x, y), (c, 0, 0, 255))
		self.progress += 1
		self.ready = self.progress == h
	def complete(self):
		while not self.ready:
			self.killtime()
	def getocean(self, depth):
		mask = pygame.mask.from_threshold(self.surf, (0, 0, 0, 255), (depth, 255, 255, 255))
		return mask.to_surface(self.ocean, setcolor = (0, 20, 60, 255), unsetcolor = (0, 0, 0, 0))


queue = []
def killtime(dt):
	tend = pygame.time.get_ticks() + 1000 * dt
	while queue and pygame.time.get_ticks() < tend:
		queue[0].killtime()
		if queue[0].ready:
			queue.pop(0)

@cache
def xPs(wP):
	return numpy.reshape(numpy.array([range(wP)], dtype = float), (wP, 1, 1))
@cache
def yPs(hP):
	return numpy.reshape(numpy.array([range(hP)], dtype = float), (1, hP, 1))

@cache
def Dx(wP, xP0, sigmaP):
	return ((xPs(wP) - xP0) / sigmaP) ** 2
@cache
def Dy(hP, yP0, sigmaP):
	return ((yPs(hP) - yP0) / sigmaP) ** 2

@lru_cache(20)
def Dgrid(wP, hP, xP0, yP0, sigmaP, d):
	return d * numpy.exp(-(Dx(wP, xP0, sigmaP) + Dy(hP, yP0, sigmaP)))

@cache
def Cgrid(rP, d = 1):
	if d != 1:
		return d * Cgrid(rP)
	ds = 1.0 - numpy.hypot(xPs(2 * rP) - rP + 0.5, yPs(2 * rP) - rP + 0.5) / rP
	a = numpy.minimum(numpy.maximum(1.0 * ds, 0.0), 1.0)
	a = a * a * (3.0 - 2.0 * a)
	return a

@cache
def anchors(size, seed):
	fs = [maff.fuzzrange(-1, 1, x, seed, 3) for x in range(size ** 2)]
	return numpy.array(fs)

def nmix(a, b, f):
	return a + (b - a) * f

def Lgrid(xGs, yGs, seed, wrap = 16):
	ix = numpy.floor(xGs).astype(int)
	iy = numpy.floor(yGs).astype(int)
	fx = xGs - ix.astype(float)
	fy = yGs - iy.astype(float)
	fx = fx * fx * (3.0 - 2.0 * fx)
	fy = fy * fy * (3.0 - 2.0 * fy)
	anchs = anchors(wrap, seed)
	ix %= wrap
	iy %= wrap
	jx = (ix + 1) % wrap
	jy = (iy + 1) % wrap
	a00 = anchs[ix + wrap * iy]
	a01 = anchs[ix + wrap * jy]
	a10 = anchs[jx + wrap * iy]
	a11 = anchs[jx + wrap * jy]
	return nmix(nmix(a00, a10, fx), nmix(a01, a11, fx), fy)

def Ngrid(xG0, yG0, wG, hG, wP, hP, seed):
	xPs = numpy.reshape(numpy.array([range(wP)], dtype = float), (wP, 1, 1))
	yPs = numpy.reshape(numpy.array([range(hP)], dtype = float), (1, hP, 1))
	xGs = numpy.broadcast_to(xG0 + xPs * (wG / wP), (wP, hP, 1))
	yGs = numpy.broadcast_to(yG0 + yPs * (hG / hP), (wP, hP, 1))

	S, C = 0.6 * 2, 0.8 * 2
	a = numpy.zeros((wP, hP, 1))
	f = 1
	for d in range(6):
		a += f * Lgrid(xGs, yGs, d + seed)
		xGs, yGs = C * xGs + S * yGs, -S * xGs + C * yGs
		f *= 0.7
	return a

@cache
def Egrid(wP, hP):
	xs = (xPs(wP) - 0.5) / wP
	ys = (yPs(hP) - 0.5) / hP
	xs = (2.0 * xs - 1.0) ** 8
	ys = (2.0 * ys - 1.0) ** 8
	return numpy.maximum(xs, ys)


class Dmap:
	def __init__(self, sizeG, PscaleG = 60, seed = 0):
		self.PscaleG = PscaleG
		self.wG, self.hG = self.sizeG = sizeG
		self.wP = int(round(self.PscaleG * self.wG))
		self.hP = int(round(self.PscaleG * self.hG))
		self.array = numpy.zeros((self.wP, self.hP, 1))
		self.array = -2.0 + 2.0 * Ngrid(0, 0, self.wG, self.hG, self.wP, self.hP, seed)
		self.array += 6.0 * Egrid(self.wP, self.hP)
		self.color0 = 30, 10, 0
		self.color1 = 140, 30, 0
		self.img0 = numpy.array(self.color0).astype(numpy.uint8).reshape((1, 1, 3))
		dcolor = numpy.array(self.color1) - numpy.array(self.color0)
		self.dimg = dcolor.astype(float).reshape((1, 1, 3))
		self.wcolor0 = 0, 0, 20
		self.wcolor1 = 0, 40, 200
		self.water0 = numpy.array(self.wcolor0).astype(numpy.uint8).reshape((1, 1, 3))
		dcolor = numpy.array(self.wcolor1) - numpy.array(self.wcolor0)
		self.dwater = dcolor.astype(float).reshape((1, 1, 3))
		self.fwater_ = None
	def drain(self, xG, yG, rG, d):
		xP = int(round(self.PscaleG * xG))
		yP = int(round(self.PscaleG * yG))
		rP = int(round(self.PscaleG * rG))
		x0, y0 = xP - rP, yP - rP
		X0, Y0 = 0, 0
		w, h = 2 * rP, 2 * rP
		if x0 >= self.wP or x0 + w <= 0: return
		if y0 >= self.hP or y0 + h <= 0: return
		if x0 < 0:
			x0, X0 = 0, -x0
			w -= X0
		if y0 < 0:
			y0, Y0 = 0, -y0
			h -= Y0
		w = min(w, self.wP - x0)
		h = min(h, self.hP - y0)
		self.array[x0:x0+w,y0:y0+h] += Cgrid(rP, d)[X0:X0+w,Y0:Y0+h]
		self.fwater_ = None
	def clip(self):
		#self.array = numpy.clip(self.array, 0.0, 1.0)
		pass
	def tosurf(self):
		carr = 1.0 / (1.0 + numpy.exp(-self.array))
		land = self.img0 + (self.dimg * carr).astype(numpy.uint8)
		water = self.water0 + (self.dwater * carr).astype(numpy.uint8)
		img = numpy.where(self.array >= 0.0, land, water)
		return pygame.surfarray.make_surface(img)
	def fwater(self):
		if self.fwater_ is None:
			self.fwater_ = numpy.count_nonzero(self.array < 0.0) / (self.wP * self.hP)
		return self.fwater_

if __name__ == "__main__":
	from . import settings, view, pview
#	settings.size0 = 500, 500
	view.init()
	hmap = Hmap(settings.size0)
	queue.append(hmap)
	clock = pygame.time.Clock()
	while not any(event.type in (pygame.KEYDOWN, pygame.QUIT) for event in pygame.event.get()):
		dt = clock.tick(60) * 0.001
		killtime(dt)
		pview.fill((0, 0, 0))
		pview.screen.blit(hmap.surf, (0, 0))
		depth = maff.imix(50, 150, maff.cycle(0.001 * pygame.time.get_ticks() / 40))
		pview.screen.blit(hmap.getocean(depth), (0, 0))
		pygame.display.flip()
		pygame.display.set_caption("%.1ffps" % clock.get_fps())


