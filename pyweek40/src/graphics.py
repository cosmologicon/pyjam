from functools import lru_cache, cache
import pygame, math
from . import pview, fuzz
from . import view
from .pview import T


def drawmask(mask, special_flags = 0):
	pview.screen.blit(mask, (0, 0), special_flags = special_flags)

@lru_cache(1)
def ssurf0(size):
	return pygame.Surface(size).convert_alpha()

def ssurf():
	return ssurf0(pview.size)

def drawlight():
	surf = ssurf()
	t = 0.001 * pygame.time.get_ticks() + 1000

	def S(omega0, omega1, *seed):
		return math.sin(fuzz.uniform(omega0, omega1, *seed) * t)
	def dx(*seed):
		return 30 * S(1, 1.5, 123, *seed) + 20 * S(2, 2.5, 234, *seed)
	def dalpha(*seed):
		return int(2 * S(0.3, 0.4, 345, *seed) + S(0.2, 0.3, 456, *seed))
	rskew = int(0.1 * pview.h)
	def drawray(x0, x1, alpha):
		ps = [(x0 + rskew, 0), (x1 + rskew, 0), (x1 - rskew, pview.h), (x0 - rskew, pview.h)]
		ps = [pview.T(p) for p in ps]
		pygame.draw.polygon(surf, (255, 255, 255, alpha), ps, 0)
	
	w0, w1 = T(600, 1000)
	x0min, x0max = -w1, pview.w + w1
	for j in range(10):
		surf.fill((255, 255, 255, 0))
		x0 = math.imix(x0min, x0max, j * math.phi % 1) + dx(j, 0)
		w = fuzz.uniform(w0, w1, 876, j)
		drawray(x0 - w + dx(j, 1), x0 + w + dx(j, 2), 4 + dalpha(j, 3))
		drawmask(surf)

def vtplus(v0, dv, f = 1):
	x0, y0 = v0
	dx, dy = dv
	return x0 + dx * f, y0 + dy * f

def bezier(p0, p1, p2, p3, t):
	p01 = math.mix(p0, p1, t)
	p12 = math.mix(p1, p2, t)
	p23 = math.mix(p2, p3, t)
	p012 = math.mix(p01, p12, t)
	p123 = math.mix(p12, p23, t)
	return math.mix(p012, p123, t)

def dbezier(p0, dp0, p1, dp1, t):
	return bezier(p0, vtplus(p0, dp0), vtplus(p1, dp1, -1), p1, t)

def drawsegment(pG0, pG1, lit = False):
	if lit:
		xV0, yV0 = view.VconvertG(pG0)
		xV1, yV1 = view.VconvertG(pG1)
		dV = view.VscaleP(0.22)
		ps = [(xV0 - dV, yV0), (xV1 - dV, yV1), (xV1 + dV, yV1), (xV0 + dV, yV0)]
		pygame.draw.polygon(pview.screen, (160, 80, 80), ps, T(2))
	else:
		pP0 = view.PconvertG(pG0)
		pP1 = view.PconvertG(pG1)
		dp0, dp1 = [(fuzz.uniform(-0.3, 0.3, 1, *pG), fuzz.uniform(0.7, 1.3, 2, *pG)) for pG in (pG0, pG1)]
		ts = [j / 20 for j in range(21)]
		pPs = [dbezier(pP0, dp0, pP1, dp1, t) for t in ts]
		pVs = [view.VconvertP(pP) for pP in pPs]
		rPs = [fuzz.uniform(0.12, 0.2, j, *pG0, *pG1) for j in range(21)]
		for pV, rP in zip(pVs, rPs):
			pygame.draw.circle(pview.screen, (80, 40, 40), pV, view.VscaleP(rP))



