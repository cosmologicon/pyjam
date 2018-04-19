from __future__ import division
import pygame
from . import settings, pview, tile, ptext
from .pview import T

S = 100
zskew = 0.7
xV0 = 640
yV0 = 440
xG0 = 0
yG0 = 0

# potentially add a third zG = 0 coordinate
def ifzG(pG):
	return pG if len(pG) == 3 else tuple(pG) + (0,)

def VconvertP(pP):
	xP, yP = pP
	return xP / pview.f, yP / pview.f
def VconvertG(pG):
	xG, yG, zG = ifzG(pG)
	xG -= xG0
	yG -= yG0
	return (
		xV0 + S * (1/2 * xG + 1/2 * yG),
		yV0 + S * (1/4 * xG - 1/4 * yG) - S * zskew * zG,
	)
def GconvertV(pV, zG = 0):
	xV, yV = pV
	zV = S * zskew * zG
	xV -= xV0
	yV -= yV0
	yV += zV
	return (
		xG0 + 1/S * (1 * xV + 2 * yV),
		yG0 + 1/S * (1 * xV - 2 * yV),
		zG,
	)
def sortkeyG(pG):
	xG, yG, zG = ifzG(pG)
	return xG - yG, zG

def GnearesttileV(pV, zG = 0):
	xG, yG, _ = GconvertV(pV, zG)
	return int(round(xG)), int(round(yG))

