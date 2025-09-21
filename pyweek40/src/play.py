import pygame
from . import pview
from . import view, grid

def think(dt):
	pass

def drawedge(pG0, pG1):
	pygame.draw.line(pview.screen, (100, 50, 50), view.VconvertG(pG0), view.VconvertG(pG1), 1) 

def drawsegment(pG0, pG1):
	xV0, yV0 = view.VconvertG(pG0)
	xV1, yV1 = view.VconvertG(pG1)
	dV = view.VscaleP(0.22)
	ps = [(xV0 - dV, yV0), (xV1 - dV, yV1), (xV1 + dV, yV1), (xV0 + dV, yV0)]
	pygame.draw.polygon(pview.screen, (80, 40, 40), ps, 0)
	


def draw():
	pview.fill((0, 0, 40))
	for pG0, pG1 in grid.segments():
		drawsegment(pG0, pG1)
	drawedge((-0.5, 0), (-0.5, 10))
	drawedge((0.5, 0), (10.5, 10))
	for yG in range(10):
		drawedge((-0.5, yG), (-0.5 + 10 - yG, 10))
		drawedge((0.5 + yG, yG), (0.5 + yG, 10))


