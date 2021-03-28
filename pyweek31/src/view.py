import math
import pygame
from . import pview
from . import settings
from .pview import T

A = math.sqrt(3) / 2  # unit hexagon apothem

camerax, cameray, cameraz = 0, 0, 60
def init():
	pview.set_mode(size0 = settings.size0, height = settings.height, fullscreen = settings.fullscreen, forceres = settings.forceres)

def clear():
	pview.screen.fill((25, 50, 25))

def distance(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	return math.hypot(x0 - x1, y0 - y1)
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

def HnearesthexH(pH):
	xH, yH = pH
	ixH, iyH = math.floor(xH), math.floor(yH)
	candidates = [(ixH, iyH), (ixH + 1, iyH), (ixH, iyH + 1), (ixH + 1, iyH + 1)]
	return min(candidates, key = lambda ipH: distance(GconvertH(ipH), GconvertH(pH)))

def VscaleG(aG):
	return T(cameraz * aG)
def VconvertG(pG):
	xG, yG = pG
	return T(pview.centerx0 + xG * cameraz, pview.centery0 - yG * cameraz)
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

