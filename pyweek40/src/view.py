import pygame
from . import pview
from . import settings

# xG, yG: grid coordinates. yG is the level, xG is the space from the left. Grid point at integers. Not rectilinear.
# xP, yP: play coordinates. yP = yG.
# xS, yS: scaled coordinates. Maps to pview.size0.
# xV, yV: view coordinates. Maps to pview.size

PxscaleG = 0.8


class camera:
	xP0 = 0
	yP0 = 3
	SscaleP = 80


def init():
	pview.set_mode(settings.size0)

def PconvertG(pG):
	xG, yG = pG
	return PxscaleG * (xG - 0.5 * yG), yG

VconvertS = pview.T

def VconvertP(pP):
	xP, yP = pP
	xS = pview.centerx0 + camera.SscaleP * (xP - camera.xP0)
	yS = pview.centery0 - camera.SscaleP * (yP - camera.yP0)
	return VconvertS((xS, yS))

def VconvertG(pG):
	return VconvertP(PconvertG(pG))


