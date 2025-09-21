import pygame, math
from . import pview
from . import settings

# xG, yG: grid coordinates. yG is the level, xG is the space from the left. Grid point at integers. Not rectilinear.
# xP, yP: play coordinates. yP = yG. Rectilinear with equal-sized unit vectors.
# xS, yS: scaled coordinates. Maps to pview.size0.
# xV, yV: view coordinates. Maps to pview.size

PxscaleG = 1.0


class camera:
	xP0 = 0
	yP0 = 4
	SscaleP = 50


def init():
	pview.set_mode(settings.size0)
	pygame.display.set_caption(settings.gamename)

def PconvertG(pG):
	xG, yG = pG
	return PxscaleG * (xG - 0.5 * yG), yG

def GconvertP(pP):
	xP, yP = pP
	return (xP + 0.5 * yP) / PxscaleG, yP

def SconvertP(pP):
	xP, yP = pP
	xS = pview.centerx0 + camera.SscaleP * (xP - camera.xP0)
	yS = pview.centery0 - camera.SscaleP * (yP - camera.yP0)
	return xS, yS

def PconvertS(pS):
	xS, yS = pS
	xP = camera.xP0 + (xS - pview.centerx0) / camera.SscaleP
	yP = camera.yP0 - (yS - pview.centery0) / camera.SscaleP
	return xP, yP

VconvertS = pview.T

def VconvertP(pP):
	return VconvertS(SconvertP(pP))

def VconvertG(pG):
	return VconvertP(PconvertG(pG))

def VscaleP(aP):
	return VconvertS(camera.SscaleP * aP)

def SscaleV(aV):
	return aV / pview.f
def SconvertV(pV):
	xV, yV = pV
	return SscaleV(xV), SscaleV(yV)

def PscaleV(aV):
	return SscaleV(aV) / camera.SscaleP
def PconvertV(pV):
	return PconvertS(SconvertV(pV))

def GnearestG(pG):
	xG, yG = pG
	return int(round(xG)), int(round(yG))

def GnearestP(pP):
	return GnearestG(GconvertP(pP))

def GnearestsegmentG(pG):
	xG, yG = pG
	yG0 = int(yG)
	yG1 = yG0 + 1
	xproj = xG - PxscaleG * (yG - yG0)
	xG0 = int(round(xproj))
	xG1 = xG0 + (1 if xproj > xG0 else 0)
	return (xG0, yG0), (xG1, yG1)

def GnearestsegmentP(pP):
	return GnearestsegmentG(GconvertP(pP))
	

def scootV(dV):
	dxV, dyV = dV
	camera.xP0 -= PscaleV(dxV)
	camera.yP0 += PscaleV(dyV)

def zoom(dz, anchorP = None):
	scale0 = camera.SscaleP
	camera.SscaleP *= math.exp(0.1 * dz)
	camera.SscaleP = math.clamp(camera.SscaleP, 10, 100)
	if anchorP is not None:
		axP, ayP = anchorP
		camera.xP0 += (axP - camera.xP0) * (1 / scale0 - 1 / camera.SscaleP)



