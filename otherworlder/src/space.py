from __future__ import division
import pygame, random, math, numpy
from pygame.locals import *
from . import pview, ptext, settings

def applyalpha(surf, alayers, offsets):
	w, h = surf.get_size()
	alpha = pygame.surfarray.pixels_alpha(surf)
	for jlayer, (alayer, (dx, dy)) in enumerate(zip(alayers, offsets)):
		if jlayer == 0:
			alpha[:,:] = alayer[dx:dx+w,dy:dy+h]
		else:
			alpha += alayer[dx:dx+w,dy:dy+h]

arrayscache = {}
def arrays(shape, Np):
	key = shape, Np
	if key not in arrayscache:
		p = shape[0] * shape[1]
		a = (numpy.arange(p) * (Np / p)).reshape(shape)
		i = numpy.floor(a)
		j = (i + 1) % Np
		f = a - i
		g = (1 - f * f * (3 - 2 * f))
		arrayscache[key] = i.astype('int'), j.astype('int'), f, g
	return arrayscache[key]

def generatelayer(size, Ns, imin, imax):
	w, h = size
	s = numpy.zeros((w, h))
	for N in Ns:
		Nw, Nh = int(round(N)), int(round(N * h / w))
		grid = numpy.random.rand(Nw * Nh) * math.tau
		yield
		Sgrid, Cgrid = numpy.sin(grid), numpy.cos(grid)
		yield
		ix, jx, fx, gx = arrays((w, 1), Nw)
		yield
		iy, jy, fy, gy = arrays((1, h), Nh)
		yield
		A0 = fx * Sgrid[ix + Nh * iy] + fy * Cgrid[ix + Nh * iy]
		yield
		A1 = fx * Sgrid[ix + Nh * jy] + (fy - 1) * Cgrid[ix + Nh * jy]
		yield
		A2 = (fx - 1) * Sgrid[jx + Nh * iy] + fy * Cgrid[jx + Nh * iy]
		yield
		A3 = (fx - 1) * Sgrid[jx + Nh * jy] + (fy - 1) * Cgrid[jx + Nh * jy]
		yield
		s += gx * gy * A0 / math.sqrt(N)
		yield
		s += gx * (1 - gy) * A1 / math.sqrt(N)
		yield
		s += (1 - gx) * gy * A2 / math.sqrt(N)
		yield
		s += (1 - gx) * (1 - gy) * A3 / math.sqrt(N)
		yield
	smin, smax = numpy.min(s), numpy.max(s)
	s = ((s - smin) * ((imax - imin) / (smax - smin)) + imin).astype('uint8')
	yield
	s = numpy.hstack([s, s])
	yield
	s = numpy.vstack([s, s])
	yield s

def getlayer(size, Ns, imin, imax):
	for layer in generatelayer(size, Ns, imin, imax):
		if layer is not None:
			return layer

screensize = None
alayers = []
dsurf = None
nlayer = 2
sgenerator = None
def generatelayers(size):
	global alayers
	alayers = []
	for _ in range(nlayer):
		for layer in generatelayer(size, [5, 8, 13, 21], 5, 255 / nlayer - 5):
			yield
			if layer is not None:
				alayers.append(layer)
				yield
def killtime(dt):
	global screensize, alayers, dsurf, sgenerator
	global sgenerator
	if settings.lowfi:
		return
	if screensize != pview.size:
		screensize = pview.size
		dsurf = pygame.Surface(pview.size).convert_alpha()
		sgenerator = generatelayers(pview.size)
		next(sgenerator)
	if not sgenerator:
		return
	endtime = pygame.time.get_ticks() + dt * 1000
	while sgenerator is not None and pygame.time.get_ticks() < endtime:
		try:
			next(sgenerator)
		except StopIteration:
			sgenerator = None

def draw(color0, color1):
	if settings.lowfi:
		pview.screen.fill(math.imix(color0, color1, 0.5))
		return
	killtime(0)
	w, h = pview.size
#	w //= 4
#	h //= 4
	directions = [math.CS(math.tau * (0.3 + jtheta / nlayer), 0.05 * 0.9 ** jtheta) for jtheta in range(nlayer)]
	t = 0.001 * pygame.time.get_ticks()
	offsets = [(int(dx * w * t) % w, int(dy * h * t) % h) for dx, dy in directions]
	pview.screen.fill(color0)
	dsurf.fill(color1)
	if alayers:
		applyalpha(dsurf, alayers, offsets[:len(alayers)])
#	pview.screen.blit(pygame.transform.scale(dsurf, pview.size), (0, 0))
	pview.screen.blit(dsurf, (0, 0))

"""
	for N in Ns:
		Nw, Nh = int(round(N)), int(round(N * h / w))
		grid = { (x, y): math.CS(random.uniform(0, math.tau)) for x in range(Nw) for y in range(Nh) }
		for x in range(w):
			for y in range(h):
				ax = x * Nw / w
				ay = y * Nh / h
				ix, iy = int(ax), int(ay)
				jx, jy = (ix + 1) % Nw, (iy + 1) % Nh
				fx, fy = ax - ix, ay - iy
				gx, gy = math.ease(1-fx), math.ease(1-fy)
				for mx, ox, kx in [(gx, fx, ix), (1-gx, fx-1, jx)]:
					for my, oy, ky in [(gy, fy, iy), (1-gy, fy-1, jy)]:
						s[x,y] += mx * my * math.dot((ox, oy), grid[(kx, ky)]) / math.sqrt(N)
	smin, smax = numpy.min(s), numpy.max(s)
	return ((s - smin) * (imax / (smax - smin))).astype('uint8')
	return numpy.random.randint(0, 50, size, 'uint8')
	surf = pygame.Surface(size).convert_alpha()
	for x in range(w):
		for y in range(h):
			c = random.randint(0, 50)
			surf.set_at((x, y), (255, 0, 0, c))
	return surf
"""

if __name__ == "__main__":
	from . import maff
	w, h = 1280, 720
#	w, h = 1280//2, 720//2
#	w, h = 300, 200
#	screen = pygame.display.set_mode((w, h))
	pview.set_mode((w, h))
	clock = pygame.time.Clock()
#	nalayer = 3
#	alayers = [getlayer((w, h), [13, 21, 34], 250/3) for _ in range(nalayer)]
#	alayers = [getlayer((w, h), [34], 250/nalayer)] * 3
#	surf = pygame.Surface((w, h)).convert_alpha()
#	directions = [math.CS(math.tau * (0.3 + jtheta / 3), r) for jtheta, r in [(0, 0.05), (1, 0.04), (2, 0.03)]]
	while not any(event.type in (KEYDOWN, QUIT) for event in pygame.event.get()):
		dt = 0.001 * clock.tick(60)
#		t = 0.001 * pygame.time.get_ticks()
#		offsets = [(int(dx * w * t) % w, int(dy * h * t) % h) for dx, dy in directions]
#		screen.fill((140, 0, 0))
#		surf.fill((0, 0, 240))
#		applyalpha(surf, alayers, offsets)
#		screen.blit(surf, (0, 0))
#		for x in (dx, dx - w):
#			for y in (dy, dy - h):
#				screen.blit(surf, (x, y), None, BLEND_ADD)
#				screen.blit(surf, (x, y))
#		draw((200, 0, 0), (0, 0, 200))
		draw((0, 0, 0), (255, 255, 255))
		ptext.draw("%.1ffps" % clock.get_fps(), (10, 10), owidth = 1)
		pygame.display.flip()

