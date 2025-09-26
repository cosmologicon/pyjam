from functools import lru_cache, cache
from collections import defaultdict
import pygame, math, os.path, random
from . import pview, fuzz, ptext
from . import view
from .pview import T

def drawmask(mask, special_flags = 0):
	pview.screen.blit(mask, (0, 0), special_flags = special_flags)

def shadeimg(surf, color):
	shade = surf.copy()
	shade.fill(color)
	shade.blit(surf, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
	return shade


@lru_cache(1)
def ssurf0(size):
	return pygame.Surface(size).convert_alpha()

def ssurf():
	return ssurf0(pview.size)

@cache
def loadimg(imgname):
	return pygame.image.load(os.path.join("img", f"{imgname}.png"))

@lru_cache(100)
def getimg0(imgname, scale = 1, angle = 0, flip_x = False, color = None):
	if scale != 1 or angle != 0:
		img = getimg0(imgname, flip_x = flip_x, color = color)
		w, h = img.get_size()
		scale /= (math.hypot(w, h) / 2)
		return pygame.transform.rotozoom(img, angle, scale)
	if flip_x:
		img = getimg0(imgname, color = color)
		return pygame.transform.flip(img, flip_x, False)
	if color is not None:
		return shadeimg(getimg0(imgname), color)
	return loadimg(imgname)
	

def getimg(imgname, scale, angle = 0, flip_x = False, color = None):
	scale = math.exp(round(math.log(scale) * 10) / 10)
	angle = round(angle / 2) * 2 % 360
	return getimg0(imgname, scale, angle, flip_x, color)

def drawimgP(pP, imgname, scaleP, angle = 0, flip_x = False, color = None):
	scaleV = view.VscaleP_continuous(scaleP)
	img = getimg(imgname, scaleV, angle, flip_x, color)
	pview.screen.blit(img, img.get_rect(center = view.VconvertP(pP)))


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

@lru_cache(100000)
def dbezier(p0, dp0, p1, dp1, t):
	return bezier(p0, math.vtplus(p0, dp0), math.vtplus(p1, dp1, -1), p1, t)

Nsegspec = 20
@lru_cache(10000)
def segmentspec(pG0, pG1, color0, color1):
	spec = []
	pP0 = view.PconvertG(pG0)
	pP1 = view.PconvertG(pG1)
	dp0, dp1 = [(fuzz.uniform(-0.3, 0.3, 1, *pG), fuzz.uniform(0.7, 1.3, 2, *pG)) for pG in (pG0, pG1)]
	ts = [j / Nsegspec for j in range(Nsegspec + 1)]
	for t in ts:
		pP = dbezier(pP0, dp0, pP1, dp1, t)
		rP = fuzz.uniform(0.12, 0.2, t, *pG0, *pG1)
		color = math.imix(color0, color1, t)
		spec.append((pP, rP, color))
	return spec

def minmaxrange(values, ws):
	minrange = min(value - w for value, w in zip(values, ws))
	maxrange = max(value + w for value, w in zip(values, ws))
	return minrange, maxrange

@lru_cache(1000)
def sphereimg(r, color = None):
	if color is not None:
		return shadeimg(sphereimg(r), color)
	surf = pygame.Surface((2 * r, 2 * r)).convert_alpha()
	for px in range(2 * r):
		x = (px - r + 0.5) / r
		for py in range(2 * r):
			y = (py - r + 0.5) / r
			d = math.hypot(x, y)
			if d > 1:
				pixel = 0, 0, 0, 0
			else:
				z = 1 - math.sqrt(d)
				a = math.interp(math.dot((x, y, z), (1, -1, 1)), 0, 0.7, 1, 1)
				pixel = math.imix((0, 0, 0, 255), (255, 255, 255, 255), a)
			surf.set_at((px, py), pixel)
	return surf


@lru_cache(1000)
def specsurf0(spec, SscaleP):
	pPs, rPs, colors = zip(*spec)
	pVs = [(view.VscaleP(xP), -view.VscaleP(yP)) for xP, yP in pPs]
	rVs = [view.VscaleP(rP) for rP in rPs]
	xVs, yVs = zip(*pVs)
	xVmin, xVmax = minmaxrange(xVs, rVs)
	yVmin, yVmax = minmaxrange(yVs, rVs)
	surf = pygame.Surface((xVmax - xVmin, yVmax - yVmin)).convert_alpha()
	surf.fill((0, 0, 0, 0))
	offset = xVmin, yVmin
	for pV, rV, color in zip(pVs, rVs, colors):
		sphere = sphereimg(rV, color)
		center = math.vminus(pV, offset)
		surf.blit(sphere, sphere.get_rect(center = center), special_flags = pygame.BLEND_RGBA_MAX)
#		pygame.draw.circle(surf, color, math.vminus(pV, offset), rV)
	return surf, offset

def specsurf(spec):
	pP0 = spec[0][0]
	spec = tuple(tuple(a) for a in spec)
	surf, offset = specsurf0(spec, view.camera.SscaleP)
	offset = math.vtplus(offset, view.VconvertP((0, 0)))
	return surf, offset

def segsurf(pG0, pG1, color0, color1):
	return specsurf(segmentspec(pG0, pG1, color0, color1))

@lru_cache(10000)
def nodecolor(pG):
	gray = fuzz.randint(15, 35, 0, *pG)
	dr = fuzz.randint(40, 80, 1, *pG)
	dg = fuzz.randint(0, 20, 2, *pG)
	db = fuzz.randint(0, 20, 3, *pG)
	return gray + dr, gray + dg, gray + db



def drawsegment(pG0, pG1, lit = False):
	if lit:
		xV0, yV0 = view.VconvertG(pG0)
		xV1, yV1 = view.VconvertG(pG1)
		dV = view.VscaleP(0.22)
		ps = [(xV0 - dV, yV0), (xV1 - dV, yV1), (xV1 + dV, yV1), (xV0 + dV, yV0)]
		pygame.draw.polygon(pview.screen, (160, 80, 80), ps, T(2))
	else:
		surf, offset = segsurf(pG0, pG1, nodecolor(pG0), nodecolor(pG1))
		pview.screen.blit(surf, offset)

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
def PstructurepartsG(pG0, pGs, color):
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
			for xH in range(xHmin, xHmax + 3):
				pHouts.append((xH - 1, yH))
	yGmax = max(yGs)
	assert len(xGs_by_yG[yGmax]) == 1
	xHmin = HscaleG * xG0
	yHmin = HscaleG * yG0
	yHmax = HscaleG * yGmax
	xHmax = HscaleG * xGs_by_yG[yGmax][0]
	pHouts += [(xHmin + dxH, yHmin - 1) for dxH in (-1, 0)]
	pHouts += [(xHmax + dxH, yHmax) for dxH in (-1, 0, 1)]
	pHouts += [(xHmax + dxH, yHmax + 1) for dxH in (0, 1)]
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
	return [(pP, 0.05, color) for pP in pPouts]

def structuresurf(pG0, pGs, color):
	return specsurf(PstructurepartsG(pG0, tuple(pGs), color))

def drawstructure(pG0, pGs, text, color0):
	if False:
		for pP, rP, color in PstructurepartsG(pG0, tuple(pGs), color0):
			pV = view.VconvertP(pP)
			rV = view.VscaleP(rP)
			pygame.draw.circle(pview.screen, color, pV, rV)
	surf, offset = structuresurf(pG0, pGs, color0)
	pview.screen.blit(surf, offset)
	ptext.draw(text, center = view.VconvertG(pG0), fontsize = view.VscaleP(0.5),
		owidth = 1)




