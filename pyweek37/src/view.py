import pygame, math
from . import pview, settings, grid

def init():
	pygame.display.init()
	pygame.display.set_caption(settings.gamename)
	pview.set_mode(size0 = settings.size0, height = settings.height,
		fullscreen = settings.fullscreen, forceres = settings.forceres)

# Coordinate systems:
#   G: game coordinates
#   V: view coordinates (size0 resolution)
#   D: display coordinates

xG0, yG0 = 0, 0
VscaleG = 100
tilt = 0.15
tip = 0.7

def scootD(dx, dy):
	global xG0, yG0
	xG0 += dx / VscaleG
	yG0 -= dy / VscaleG

def zoomto(scale):
	global VscaleG
	VscaleG = min(settings.zooms, key = lambda zoom: abs(math.log(scale / zoom)))

def zoomstep(d = 1, pDanchor = None):
	if d >= 0:
		j = sum(zoom <= VscaleG for zoom in settings.zooms) + d
	else:
		j = sum(zoom < VscaleG for zoom in settings.zooms) + d
	zoom(settings.zooms[math.clamp(j, 0, len(settings.zooms) - 1)], pDanchor)

def zoom(scale, pDanchor = None):
	global xG0, yG0, VscaleG
	xV0, yV0 = pview.center
	xVanchor, yVanchor = VconvertD(pDanchor or pview.center)
	oldVscaleG = VscaleG
	VscaleG = scale
	VscaleG = math.clamp(VscaleG, 10, 200)
	# xG(xVanchor) = xG0 + (xVanchor - xV0) / VscaleG is a constant
	# oldxG0 + (xVanchor - xV0) / oldVscaleG = xG0 + (xVanchor - xV0) / VscaleG0
	xG0 += (xVanchor - xV0) * (1 / oldVscaleG - 1 / VscaleG)
	yG0 -= (yVanchor - yV0) * (1 / oldVscaleG - 1 / VscaleG)

def VconvertG(pG, zG = 0):
	xV0, yV0 = pview.center
	xG, yG = math.R(tilt, pG)
	yG, zG = math.R(-tip, (yG, zG))
	return xV0 + VscaleG * (xG - xG0), yV0 - VscaleG * (yG - yG0)

def GconvertV(pV):
	xV0, yV0 = pview.center
	xV, yV = pV
	xG, yG = xG0 + (xV - xV0) / VscaleG, yG0 - (yV - yV0) / VscaleG
	yG /= math.cos(tip)
	return math.R(-tilt, (xG, yG))

def VconvertD(pD):
	xD, yD = pD
	return xD / pview.f, yD / pview.f

def DconvertV(pV):
	return pview.T(pV)

def DconvertG(pG, zG = 0):
	return DconvertV(VconvertG(pG, zG))

def GconvertD(pD):
	return GconvertV(VconvertD(pD))
	
def DscaleG(pG):
	return pview.T(VscaleG * pG)

def DconvertH(pH):
	return DconvertG(grid.GconvertH(pH))
