from functools import lru_cache, cache
from collections import defaultdict
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

def bezier(p0, p1, p2, p3, t):
	p01 = math.mix(p0, p1, t)
	p12 = math.mix(p1, p2, t)
	p23 = math.mix(p2, p3, t)
	p012 = math.mix(p01, p12, t)
	p123 = math.mix(p12, p23, t)
	return math.mix(p012, p123, t)

def dbezier(p0, dp0, p1, dp1, t):
	return bezier(p0, math.vtplus(p0, dp0), math.vtplus(p1, dp1, -1), p1, t)

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

HscaleG = 4
def HconvertG(pG):
	xG, yG = pG
	return HscaleG * xG, HscaleG * yG
def GconvertH(pH):
	xH, yH = pH
	return xH / HscaleG, yH / HscaleG
def PconvertH(pH):
	return view.PconvertG(GconvertH(pH))

@lru_cache(1000)
def PstructurepartsG(pG0, pGs):
	xG0, yG0 = pG0
	xGs_by_yG = defaultdict(list)
	xGs_by_yG[yG0].append(xG0)
	for xG, yG in pGs:
		xGs_by_yG[yG].append(xG)
	yGs = sorted(xGs_by_yG)
	pHouts = []
	for yGlo in yGs[:-1]:
		yGhi = yGlo + 1
		xGlomin = min(xGs_by_yG[yGlo])
		xGlomax = max(xGs_by_yG[yGlo])
		xGhimin = min(xGs_by_yG[yGhi])
		xGhimax = max(xGs_by_yG[yGhi])
		for dH in range(HscaleG):
			f, g = HscaleG - dH, dH
			yH = f * yGlo + g * yGhi
			xHmin = f * xGlomin + g * xGhimin
			xHmax = f * xGlomax + g * xGhimax
			for xH in range(xHmin, xHmax + 4):
				pHouts.append((xH - 1.5, yH))
	yGmax = max(yGs)
	assert len(xGs_by_yG[yGmax]) == 1
	xHmin = HscaleG * xG0
	yHmin = HscaleG * yG0
	yHmax = HscaleG * yGmax
	xHmax = HscaleG * xGs_by_yG[yGmax][0]
	pHouts += [(xHmin + dxH, yHmin - 2) for dxH in (-1.5, -0.5)]
	pHouts += [(xHmin + dxH, yHmin - 1) for dxH in (-1.5, -0.5, 0.5)]
	pHouts += [(xHmax + dxH, yHmax) for dxH in (-1.5, -0.5, 0.5, 1.5)]
	pHouts += [(xHmax + dxH, yHmax + 1) for dxH in (-0.5, 0.5, 1.5)]
	pHsegs = []
	for pH in pHouts:
		pHbelows = [math.vtplus(pH, dpH) for dpH in [(-1, -1), (0, -1)]]
		pHbelows = [pHbelow for pHbelow in pHbelows if pHbelow in pHouts]
		if pHbelows:
			pHbelow = fuzz.choice(pHbelows, *pH)
			pHsegs.append((pHbelow, pH))
	pPsegs = [(PconvertH(pH0), PconvertH(pH1)) for pH0, pH1 in pHsegs]
	pPouts = []
	def dP(pP):
		dP0 = 1 / HscaleG
		wP = 0.4 / HscaleG
		return fuzz.uniform(-wP, wP, 0, *pP), dP0 + fuzz.uniform(-wP, wP, 1, *pP)
	for pP0, pP1 in pPsegs:
		for jt in range(20):
			pPouts.append(dbezier(pP0, dP(pP0), pP1, dP(pP1), jt / 19))
	return [(pP, 0.05) for pP in pPouts]
	

def drawstructure(pG0, pGs):
	for pP, rP in PstructurepartsG(pG0, tuple(pGs)):
		pV = view.VconvertP(pP)
		rV = view.VscaleP(rP)
		pygame.draw.circle(pview.screen, (70, 60, 40), pV, rV)





