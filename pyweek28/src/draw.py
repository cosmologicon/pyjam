# Draw world objects (i.e. in the middle panel)

from __future__ import division
import pygame, math, random, numpy
from functools import lru_cache  # TODO: backfill to support Python 2
from . import pview, state, view
from .pview import T


def randomstar():
	z = random.uniform(0, 10000)
	A = random.uniform(0, 8)
	depth = random.randint(2, 10)
	num = int(random.uniform(100, 255) * depth / 10)
	color = (num, num, num)
	return z, A, depth, color
stardata = [randomstar() for _ in range(10000)]


# TODO: restrict to the central viewing area.
_laststarz = None  # Last z-position so we can stretch the stars accordingly.
def stars():
	global _laststarz
	if _laststarz is None: _laststarz = view.zW0
	dy = [int(round(0.3 * (view.zW0 - _laststarz) * depth * pview.f)) for depth in range(11)]
	A0 = 0.000005 * pygame.time.get_ticks()
	pview.fill((0, 0, 0))
	Nstar = int(round(1500 * pview.area / pview.area0))
	for z, A, depth, color in stardata[:Nstar]:
		# TODO: dynamically change with camera zoom level
		px, py = T(pview.centerx0 + 500 * view.dA(A, view.A - A0 * depth), -6 * depth * (z - view.zW0) % pview.h0)
		if _laststarz == view.zW0:
			pview.screen.set_at((px, py), color)
		else:
			c = pview.I(color[0] / math.clamp(abs(dy[depth]) / 4, 1, 10))
			pygame.draw.line(pview.screen, (c, c, c), (px, py + dy[depth]), (px, py - dy[depth]))
	_laststarz = view.zW0

def atmosphere():
	# Atmosphere
	alpha = pview.I(math.fadebetween(view.zW0, 10, 255, 100, 0))
	if alpha:
		pview.fill((0, 40, 80, alpha))
def ground():
	_, py = view.gametoview((0, -2))
	if py <= pview.h:
		pview.screen.fill((0, 10, 0), pygame.Rect(0, py, pview.w, pview.h))


# Okay, here we go....

# The 3-D effect is achieved by constructing a numpy array to sample from a texture, which is a
# separately constructed pygame.Surface object.
# Every element in 3-D is an axially symmetric shape with a radius defined as a function with
# respect to height. We use an axis-aligned orthographic projection to determine the texture
# coordinates as a function of position within the image.
# Honestly, I'll need a whiteboard and an hour to explain most of these variables.
# See the notebook entry date 24 Sep 2019.
@lru_cache(40)
def getelement(tname, w, h, r0, r1, n, A0, k):
	texture = gettexture(tname)
	w0, h0, _ = texture.shape
	x = numpy.arange(w).reshape(w, 1)
	y = numpy.arange(h).reshape(1, h)
	b = 1 - (y + 1/2) / h
	if r0 != r1:
		r = getr(b, r0, r1, n)
	else:
		# If r0 == r1, then a lot of the 2-d arrays don't change vertically, and be treated as 1-d
		# arrays until it's time to broadcast.
		r = r0
	a = (x + (1/2 - w/2)) / r
	mask = abs(a) <= 1
	G = numpy.arcsin(a * mask)
	u = k * (G / math.tau - A0 / 8)
	v = 1 - b
	# Shading
	g = a + 0.4 * (a ** 2 - 1)
	f = 1 - abs(g ** 2)
	U = (u * w0 + 1/2).astype(int) % w0 * mask
	V = (v * h0 + 1/2).astype(int) % h0
	fw, fh = f.shape
	f = f.reshape(fw, fh, 1)

	surf = pygame.Surface((w, h)).convert_alpha()
	arr = pygame.surfarray.pixels3d(surf)
	arr[:, :, :] = (texture[U, V, :] * f).astype(int)
	del arr
	pygame.surfarray.pixels_alpha(surf)[:,:] = 255 * mask
	return surf

@lru_cache(None)
def gettexture(tname):
	if tname == "cable":
		surf = getcablesurf()
	elif tname == "window":
		surf = pygame.Surface((10, 10)).convert()
		surf.fill((100, 100, 100))
		surf.fill((100, 150, 255), pygame.Rect(1, 1, 8, 8))
	elif tname == "lowwindow":
		surf = pygame.Surface((10, 10)).convert()
		surf.fill((100, 100, 100))
		surf.fill((100, 150, 255), pygame.Rect(1, 5, 8, 4))
	elif tname.startswith("solid-"):
		surf = pygame.Surface((1, 1)).convert()
		surf.fill(pygame.Color(tname[6:]))
	elif tname.startswith("stripe-"):
		surf = pygame.Surface((1, 4)).convert()
		surf.fill((100, 100, 100))
		surf.set_at((0, 2), pygame.Color(tname[7:]))
#		surf.set_at((0, 3), pygame.Color(tname[7:]))
	elif tname == "roundtop":
		surf = pygame.Surface((200, 100)).convert()
		surf.fill((60, 60, 60))
		pygame.draw.circle(surf, (40, 40, 80), (100, 100), 80)
		pygame.draw.circle(surf, (80, 80, 80), (100, 100), 50)
	elif tname == "gray":
		surf = pygame.Surface((1, 1)).convert()
		surf.fill((120, 120, 120))
	elif tname == "rock":
		surf = pygame.Surface((100, 100)).convert()
		pygame.surfarray.pixels3d(surf)[:,:] = (numpy.random.random_sample((100, 100, 1)) * 10 + 60).astype(int)
	elif tname == "hatch":
		w = 20
		surf = pygame.Surface((w, 1)).convert()
		for x in range(w):
			c = int(round(math.mix(80, 120, math.cycle(x / w))))
			surf.set_at((x, 0), (c, c, c))
	else:
		raise ValueError
	return pygame.surfarray.pixels3d(surf)

# r (radius of the element) with respect to b (vertical position).
# n is the ratio of the slope: n = dr(1)/db / dr(0)/db
# n = 1 is flat, n < 1 is concave, n > 1 is convex.
def getr(b, r0, r1, n):
	if n == 1: return r0 + (r1 - r0) * b
	D = (n * r0 - r1) / (n - 1)
	E = (r1 - r0) / (n - 1)
	F = math.log(n)
	return D + E * numpy.exp(F * b)

def drawelement(tname, xG, y0G, y1G, r0, r1, n, A0, k):
	x0, y0 = view.gametoview((xG, y0G))
	x0, y1 = view.gametoview((xG, y1G))
	if (y0 < 0 and y1 < 0) or (y0 > pview.h and y1 > pview.h): return
	r0 = T(view.zoom * r0)
	r1 = T(view.zoom * r1)
	w = int(math.ceil(2 * max(r0, r1)))
	h = y0 - y1
	surf = getelement(tname, w, h, r0, r1, n, A0, k)
	rect = surf.get_rect(midbottom = (x0, y0))
	if pview.rect.colliderect(rect):
		pview.screen.blit(surf, rect)

# Drawing the central cable
def getcablesurf():
	w, h = 800, 400
	surf = pygame.Surface((w, h)).convert()
	surf.fill((80, 80, 80))
	for _ in range(100):
		# Stripe slope
		d = random.choice([1, 3, 5])
		n = random.randint(1, d // 2 + 1)
		flip = random.choice([False, True])
		n, d = (1, 3) if flip else (3, 5)
		xstep = pview.I(1 / d * w)
		dx = xstep * n
		# Stripe width
		s = random.randint(5, 10)
		color0 = random.randint(84, 90)
		color = [color0 + random.randint(-1, 1) for _ in range(3)]
		x0 = random.randint(0, w)
		y0, y1 = (0, h) if flip else (h, 0)
		while x0 + dx + s > 0:
			x0 -= xstep
		while x0 < w:
			ps = (x0, y0), (x0 + dx, y1), (x0 + dx + s, y1), (x0 + s, y0)
			pygame.draw.polygon(surf, color, ps)
			x0 += xstep
	# Tracks
	for A in range(9):
		x = int(round(A / 8 * w))
		a = int(round(w / 60))
		pygame.draw.line(surf, (70, 70, 70), (x, 0), (x, h), a)
	return surf

# Main entry point.
_lastcablez = None
def cable():
	global _lastcablez
	if _lastcablez is None: _lastcablez = view.zW0
	r = T(state.radius * view.zoom)
	w = 2 * r
	h = int(round(r * math.pi))
	surf = getelement("cable", w, h, r, r, 1, view.A, 1)
	dz = max(1, 0.3 * abs(_lastcablez - view.zW0))
	if dz > 1:
		h2 = max(1, int(round(h / dz)))
		surf2 = pygame.transform.smoothscale(surf, (w, h2))
		surf = pygame.transform.smoothscale(surf2, (w, h))
	hfull = T(state.top * view.zoom)
	# TODO: make this calculation more stable to small changes in view.zoom.
	xV, yV = view.gametoview((0, 0))
	# TODO: cut off at the top of the tower (or maybe just draw something over it so it looks like
	# the end.
	if yV - pview.h > h:
		yV = (yV - pview.h) % h + pview.h
	while yV > 0:
		rect = surf.get_rect(midbottom=(xV, yV))
		pview.screen.blit(surf, rect)
		yV -= h
	_lastcablez = view.zW0

def sparkdatum():
	pW = math.norm([random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)])
	speed = random.uniform(2, 4)
	return pW, speed

sparkdata = [sparkdatum() for _ in range(1000)]
def sparks(pW):
	x0, y0, z0 = pW
	if not view.visible(z0, 5):
		return
	Nspark = int(round(100 * pview.f))
	t = pygame.time.get_ticks() * 0.001
	for (dx, dy, dz), speed in sparkdata[:Nspark]:
		jcolor, dt = divmod(t * speed, 1)
		color = [(255,255,255),(255,200,200),(255,225,200),(255,255,180),(200,200,255)][int(jcolor % 5)]
		dt **= 2.5
		dt += 0.3 * speed
		p0 = x0 + dx * dt, y0 + dy * dt, z0 + dz * dt - 0.1 * dt ** 2
		dt += 0.05 * speed
		p1 = x0 + dx * dt, y0 + dy * dt, z0 + dz * dt - 0.1 * dt ** 2
		pygame.draw.line(pview.screen, color, view.worldtoview(p0), view.worldtoview(p1))	
		
		
	

