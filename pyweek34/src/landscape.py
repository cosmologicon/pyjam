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
	d2s = 1.0 - ((xPs(2 * rP) - rP + 0.5) / rP) ** 2 - ((yPs(2 * rP) - rP + 0.5) / rP) ** 2
	a = numpy.minimum(numpy.maximum(2.0 * d2s, 0.0), 1.0)
	a = numpy.sqrt(a)
	a = a * a * (3.0 - 2.0 * a)
	return a


class Dmap:
	def __init__(self, size, scale = 60):
		self.scale = scale
		self.wG, self.hG = self.size = size
		self.wP = int(round(self.wG * scale))
		self.hP = int(round(self.hG * scale))
		self.array = numpy.zeros((self.wP, self.hP, 1))
		self.color0 = 60, 20, 0
		self.color1 = 140, 30, 0
		self.img0 = numpy.array(self.color0).astype(numpy.uint8).reshape((1, 1, 3))
		dcolor = numpy.array(self.color1) - numpy.array(self.color0)
		self.dimg = dcolor.astype(float).reshape((1, 1, 3))
	def drain(self, xG, yG, rG, d):
		xP = int(round(xG * self.scale))
		yP = int(round(yG * self.scale))
		rP = int(round(rG * self.scale))
		print()
		x0, y0 = xP - rP, yP - rP
		X0, Y0 = 0, 0
		w, h = 2 * rP, 2 * rP
		print(x0, y0, X0, Y0, w, h)
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
		print(x0, y0, X0, Y0, w, h)
		self.array[x0:x0+w,y0:y0+h] += Cgrid(rP, d)[X0:X0+w,Y0:Y0+h]
	def tosurf(self):
		img = self.img0 + (self.dimg * self.array).astype(numpy.uint8)
		return pygame.surfarray.make_surface(img)

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


