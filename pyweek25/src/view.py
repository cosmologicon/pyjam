from __future__ import division
import pygame, math
from . import settings, pview, ptext
from .pview import T

xV0 = 640
yV0 = 440
xG0 = 0
yG0 = 0

# a = arctan(1 / phi)
sina = 1 / math.sqrt(math.phi + 2)
cosa = math.phi * sina

# b = arccos(1/2)
sinb = math.sqrt(3) / 2
cosb = 1/2

IscaleG = 100

# potentially add a third zG = 0 coordinate
def ifzG(pG):
	return pG if len(pG) == 3 else tuple(pG) + (0,)

def VconvertP(pP):
	xP, yP = pP
	return xP / pview.f, yP / pview.f
def IconvertG(pG):
	xG, yG, zG = ifzG(pG)
	xG -= xG0
	yG -= yG0
	return (
		IscaleG * (cosa * xG + sina * yG),
		IscaleG * (sina * xG - cosa * yG),
		IscaleG * zG
	)

def VconvertG(pG):
	xI, yI, zI = IconvertG(pG)
	return (
		xV0 + xI,
		yV0 + cosb * yI - sinb * zI
	)
def GconvertV(pV, zG = 0):
	xV, yV = pV
	xV -= xV0
	yV -= yV0
	xI = xV
	zI = zG / IscaleG
	yI = (yV + sinb * zI) / cosb
	return (
		xG0 + (cosa * xI + sina * yI) / IscaleG,
		yG0 + (sina * xI - cosa * yI) / IscaleG,
		zG,
	)
def sortkeyG(pG):
	xG, yG, zG = ifzG(pG)
	return xG - yG, zG

def GnearesttileV(pV, zG = 0):
	xG, yG, _ = GconvertV(pV, zG)
	return int(round(xG)), int(round(yG))

