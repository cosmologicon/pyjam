import math, functools
import pygame
from . import pview
from . import settings, state
from .pview import T
cache = functools.lru_cache(None)

A = math.sqrt(3) / 2  # unit hexagon apothem

pview.SCREENSHOT_DIRECTORY = "screenshots"

zooms = [20, 25, 30, 40, 50, 60]
camerax, cameray, cameraz = 0, 0, 40
def init():
	pview.set_mode(size0 = settings.size0, height = settings.height, fullscreen = settings.fullscreen, forceres = settings.forceres)
	pygame.display.set_caption(settings.gamename)

def resize():
	pview.cycle_height(settings.heights)
	settings.height = pview.height
	settings.save()
	from . import graphics
	graphics.reset()

def toggle_fullscreen():
	settings.fullscreen = not settings.fullscreen
	pview.set_mode(fullscreen = settings.fullscreen)
	settings.save()
	from . import graphics
	graphics.reset()

def clear():
	pview.screen.fill((25, 50, 25))

def reset():
	global camerax, cameray, cameraz
	camerax, cameray = 0, 0
	zs = [z for z in zooms if 2 * state.R * z <= pview.h0]
	cameraz = max(zs) if zs else min(zooms)

def zoom(dz, mposV = None):
	global camerax, cameray, cameraz
	if mposV is None:
		mposV = pview.center
	(xG0, yG0) = GconvertV(mposV)
	cameraz = zooms[math.clamp(zooms.index(cameraz) + dz, 0, len(zooms) - 1)]
	(xG1, yG1) = GconvertV(mposV)
	camerax -= xG1 - xG0
	cameray -= yG1 - yG0

def pan(dpV):
	global camerax, cameray
	dxV, dyV = dpV
	camerax -= GscaleV(dxV)
	cameray += GscaleV(dyV)

def snap(dt):
	global camerax, cameray
	r = state.R + 2
	wG, hG = GscaleV(pview.w), GscaleV(pview.h)
	x0 = abs(wG / 2 - r)
	y0 = abs(hG / 2 - r)
	if camerax > x0: camerax = math.softapproach(camerax, x0, 10 * dt)
	if camerax < -x0: camerax = math.softapproach(camerax, -x0, 10 * dt)
	if cameray > y0: cameray = math.softapproach(cameray, y0, 10 * dt)
	if cameray < -y0: cameray = math.softapproach(cameray, -y0, 10 * dt)


def vecadd(p0, p1, f = 1):
	x0, y0 = p0
	x1, y1 = p1
	return x0 + f * x1, y0 + f * y1


# N, NE, SE, S, SW, NW
dirHs = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
cornerdHs = [(1/3, 1/3), (2/3, -1/3), (1/3, -2/3), (-1/3, -1/3), (-2/3, 1/3), (-1/3, 2/3)]

# Units of angles are sixths of a rotation clockwise, i.e. angle = 1 is N => NE.
def HrotH(pH, angle = 1):
	angle %= 6
	xH, yH = pH
	if angle >= 3:
		xH, yH = -xH, -yH
		angle -= 3
	while angle > 0:
		xH, yH = xH + yH, -xH
		angle -= 1
	return xH, yH

def GconvertH(pH):
	xH, yH = pH
	return 3/2 * xH, A * (xH + 2 * yH)
# https://www.wolframalpha.com/input/?i=inverse+of+matrix+%7B%7B3%2F2%2C0%7D%2C%7BA%2C2A%7D%7D
def HconvertG(pG):
	xG, yG = pG
	return 2/3 * xG, -1/3 * xG + yG / (2 * A)
def GoutlineH(pH, f = 1):
	return [GconvertH(vecadd(pH, dH, f)) for dH in cornerdHs]

def HnearesthexH(pH):
	xH, yH = pH
	ixH, iyH = math.floor(xH), math.floor(yH)
	candidates = [(ixH, iyH), (ixH + 1, iyH), (ixH, iyH + 1), (ixH + 1, iyH + 1)]
	return min(candidates, key = lambda ipH: math.distance(GconvertH(ipH), GconvertH(pH)))
@cache
def HsurroundH(pH, r = 1):
#	if pH != (0, 0):
#		return set(vecadd(pH, tile) for tile in HsurroundH((0, 0), r))
	if r == 0:
		return set([pH])
	tiles = HsurroundH(pH, r-1)
	return tiles | set(vecadd(tile, dirH) for tile in tiles for dirH in dirHs)
@cache
def Hfill(R):
	r = int(math.ceil(R / math.sqrt(3)))
	return [pH for pH in HsurroundH((0, 0), r) if math.hypot(*GconvertH(pH)) < R]

gridedgeGs = [
	(GconvertH(pH0), GconvertH(pH1)) for pH0, pH1 in set([
		(vecadd(pH, HrotH((1, 1), j), 1/3), vecadd(pH, HrotH((1, 1), j + 1), 1/3))
		for pH in HsurroundH((0, 0), 12)
		for j in range(6)
		if math.hypot(*GconvertH(pH)) < 17.4
	])
]

def VscaleG(aG):
	return T(cameraz * aG)
def GscaleV(aV):
	return aV / cameraz / pview.f
def VconvertG(pG):
	xG, yG = pG
	return T(pview.centerx0 + (xG - camerax) * cameraz, pview.centery0 - (yG - cameray) * cameraz)
def GconvertV(pV):
	xV, yV = pV
	return (
		camerax + (xV - pview.centerx) / (cameraz * pview.f),
		cameray - (yV - pview.centery) / (cameraz * pview.f),
	)

def VconvertH(pH):
	return VconvertG(GconvertH(pH))
def HconvertV(pV):
	return HconvertG(GconvertV(pV))

