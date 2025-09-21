import pygame
from . import pview
from . import view

def think(dt):
	pass

def draw():
	pview.fill((0, 0, 40))

	def drawedge(pG0, pG1):
		pygame.draw.line(pview.screen, (100, 50, 50), view.VconvertG(pG0), view.VconvertG(pG1), 1) 

	drawedge((-0.5, 0), (-0.5, 10))
	drawedge((0.5, 0), (10.5, 10))
	for yG in range(10):
		drawedge((-0.5, yG), (-0.5 + 10 - yG, 10))
		drawedge((0.5 + yG, yG), (0.5 + yG, 10))


