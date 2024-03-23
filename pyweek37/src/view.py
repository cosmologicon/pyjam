import pygame, math
from . import pview, settings, grid

def init():
	pygame.display.init()
	pygame.display.set_caption(settings.gamename)
	pview.set_mode(size0 = settings.size0, height = settings.height,
		fullscreen = settings.fullscreen, forceres = settings.forceres)

def toggleresolution():
	pview.cycle_height(settings.heights)
	settings.height = pview.height
	settings.save()

def togglefullscreen():
	settings.fullscreen = not settings.fullscreen
	pview.set_mode(fullscreen = settings.fullscreen)
	settings.save()



# Coordinate systems:
#   G: game coordinates
#   V: view coordinates (size0 resolution)
#   D: display coordinates

xG0, yG0 = 0, 0
VscaleG = 100
tilt = 0.15
tip = 0.7

def scootD(dpD):
	from . import state
	global xG0, yG0
	dxD, dyD = dpD
	VscaleD = 1 / pview.f
	dxG, dyG = VscaleD * dxD / VscaleG, -VscaleD * dyD / VscaleG
	dyG /= math.cos(tip)
	dxG, dyG = math.R(-tilt, (dxG, dyG))
	xG0 += dxG / 3.5
	yG0 += dyG / 3.5
	xG0 = math.clamp(xG0 + dxG, state.minxG, state.maxxG)
	yG0 = math.clamp(yG0 + dyG, state.minyG, state.maxyG)

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
	VscaleG = math.clamp(VscaleG, settings.minzoom, settings.maxzoom)
	# xG(xVanchor) = xG0 + (xVanchor - xV0) / VscaleG is a constant
	# oldxG0 + (xVanchor - xV0) / oldVscaleG = xG0 + (xVanchor - xV0) / VscaleG0
	xG0 += (xVanchor - pview.centerx0) * (1 / oldVscaleG - 1 / VscaleG)
	yG0 -= (yVanchor - pview.centery0) * (1 / oldVscaleG - 1 / VscaleG)

def VconvertG(pG, zG = 0):
	xG, yG = pG
	dxG = xG - xG0
	dyG = yG - yG0
	dxG, dyG = math.R(tilt, (dxG, dyG))
	dyG, zG = math.R(-tip, (dyG, zG))
	return pview.centerx0 + VscaleG * dxG, pview.centery0 - VscaleG * dyG

def GconvertV(pV):
	xV, yV = pV
	dxG, dyG = (xV - pview.centerx0) / VscaleG, -(yV - pview.centery0) / VscaleG
	dyG /= math.cos(tip)
	dxG, dyG = math.R(-tilt, (dxG, dyG))
	return xG0 + dxG, yG0 + dyG

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
