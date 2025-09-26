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
	SscaleP = 70
	minzoom = 60
	maxzoom = 100
	ceilingP = 9.5
	floorP = -2
	wallP = 10

def setceiling(h):
	newceiling = h + 0.5
	if h <= 12:
		camera.yP0 += newceiling - camera.ceilingP
	camera.ceilingP = newceiling
	camera.floorP = 0
	camera.wallP = newceiling * 0.5
	camera.minzoom = min(100, 640 / h)
	camera.maxzoom = 100
	camera.SscaleP = math.clamp(camera.SscaleP, camera.minzoom, camera.maxzoom)
	enforce()

def enforce():
	xSmid, ySmid = pview.center
	xPmax = camera.wallP - xSmid / camera.SscaleP
	if xPmax <= 0:
		camera.xP0 = 0
	else:
		camera.xP0 = math.clamp(camera.xP0, -xPmax, xPmax)
	yPmin = camera.floorP + ySmid / camera.SscaleP
	yPmax = camera.ceilingP - ySmid / camera.SscaleP
	if yPmin > yPmax:
		camera.yP0 = yPmax
	else:
		camera.yP0 = math.clamp(camera.yP0, yPmin, yPmax)


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

def VscaleP_continuous(aP):
	return pview.f * camera.SscaleP * aP

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
	xproj = xG - 0.5 * (yG - yG0)
	xG0 = int(round(xproj))
	xG1 = xG0 + (1 if xproj > xG0 else 0)
	return (xG0, yG0), (xG1, yG1)

assert GnearestsegmentG((-0.2, 0.4)) == ((0, 0), (0, 1))

def GnearestsegmentP(pP):
	return GnearestsegmentG(GconvertP(pP))


def scootV(dV):
	dxV, dyV = dV
	camera.xP0 -= PscaleV(dxV)
	camera.yP0 += PscaleV(dyV)
	enforce()

def zoom(dz, anchorP = None):
	scale0 = camera.SscaleP
	camera.SscaleP *= math.exp(0.1 * dz)
	camera.SscaleP = math.clamp(camera.SscaleP, camera.minzoom, camera.maxzoom)
	if anchorP is not None:
		axP, ayP = anchorP
		camera.xP0 += (axP - camera.xP0) * (1 / scale0 - 1 / camera.SscaleP)
	enforce()


