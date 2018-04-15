from __future__ import division
import pygame
from . import settings, pview, tile, ptext
from .pview import T

S = 160
xV0 = 640
yV0 = 520
xG0 = 0
yG0 = 0

def VconvertG(pG):
	xG, yG = pG
	xG -= xG0
	yG -= yG0
	return [
		xV0 + S * (1/2 * xG + 1/2 * yG),
		yV0 + S * (1/4 * xG - 1/4 * yG),
	]
def sortkeyG(pG):
	xG, yG = pG
	return xG - yG

def drawtile(color, pG):
	tile.draw(color, VconvertG(pG), 0.94 * S)

def drawpiece(name, color, pG):
	xV, yV = VconvertG(pG)
	ps = [T(xV + S * a, yV + S * b) for a, b in
		[(0.25, 0), (-0.25, 0), (-0.15, -0.6), (0.15, -0.6)]]
	pygame.draw.polygon(pview.screen, pygame.Color(color), ps)
	pygame.draw.lines(pview.screen, pygame.Color("black"), True, ps, T(0.05 * S))
	ptext.draw(name, center = T(xV, yV - S * 0.25), fontsize = T(0.35 * S), color = "white",
		ocolor = "black", owidth = 1)

