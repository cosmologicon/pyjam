import pygame
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
VscaleG = 100  # VscaleG

def scoot(dx, dy):
	global xG0, yG0
	xG0 += 600 * dx / VscaleG
	yG0 += 600 * dy / VscaleG

def VconvertG(pG):
	xV0, yV0 = pview.center
	xG, yG = pG
	return [xV0 + VscaleG * (xG - xG0), yV0 - VscaleG * (yG - yG0)]

def GconvertV(pV):
	xV0, yV0 = pview.center
	xV, yV = pV
	return [xG0 + (xV - xV0) / VscaleG, yG0 - (yV - yV0) / VscaleG]

def VconvertD(pD):
	xD, yD = pD
	return [xD / pview.f, yD / pview.f]

def DconvertV(pV):
	return pview.T(pV)

def DconvertG(pG):
	return DconvertV(VconvertG(pG))

def GconvertD(pD):
	return GconvertV(VconvertD(pD))
	
def DscaleG(pG):
	return pview.T(VscaleG * pG)

def DconvertH(pH):
	return DconvertG(grid.GconvertH(pH))
