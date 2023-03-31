import pygame, math
from . import settings
from . import pview
from .pview import T

# isometric dimension ratio
iso = 0.5
siso = math.sqrt(1 - iso ** 2)

xG0, yG0 = 0, 0
VscaleG = 40

def init():
	pview.set_mode(size0 = settings.size0, height = settings.height,
		fullscreen = settings.fullscreen, forceres = settings.forceres)
	pygame.display.set_caption(settings.gamename)

def set_camera(xG0_, yG0_, VscaleG_):
	global xG0, yG0, VscaleG
	xG0, yG0, VscaleG = xG0_, yG0_, VscaleG_

def VconvertG(pG, zG = 0):
	xG, yG = pG
	xV = pview.centerx0 + (xG - xG0) * VscaleG
	yV = pview.centery0 - (yG - yG0) * VscaleG * iso - zG * VscaleG * siso
	return T(xV, yV)

def GconvertV(pV):
	xV, yV = pV
	xG = xG0 + (xV - pview.centerx0) / VscaleG
	yG = yG0 - (yV - pview.centery0) / VscaleG / iso
	return xG, yG

def box(pGs):
	xGs, yGs = zip(*pGs)
	return (min(xGs), min(yGs)), (max(xGs), max(yGs))

def framegrid(grid):
	(xG0, yG0), (xG1, yG1) = box(grid.pGs())
	xG = (xG1 + xG0) / 2
	yG = (yG1 + yG0) / 2
	xscale = pview.w0 / (xG1 - xG0 + 5)
	yscale = pview.h0 / (yG1 - yG0 + 5) / iso
	scale = min(xscale, yscale)
	print(xG1 - xG0, yG1 - yG0, xscale, yscale, scale)
	set_camera(xG, yG, scale)


