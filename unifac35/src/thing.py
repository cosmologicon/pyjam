import pygame
from . import pview, grid, view
from .pview import T

def drawcircleat(pH, rG, color):
	xG, yG = grid.GconvertH(pH)
	xV, yV = view.VconvertG((xG, yG))
	r = T(view.VscaleG * rG)
	h = T(view.VscaleG * rG * 0.6)
	pygame.draw.circle(pview.screen, color, (xV, yV - h), r)


class You:
	def __init__(self, pH):
		self.pH = pH

	def draw0(self):
		drawcircleat(self.pH, 0.4, (255, 200, 40))

class Obstacle:
	def __init__(self, pH):
		self.pH = pH

	def draw0(self):
		drawcircleat(self.pH, 0.3, (255, 255, 255))


class Light:
	def __init__(self, grid, pH, dirHs):
		self.grid = grid
		self.pH = pH
		self.dirHs = dirHs

	def illuminate(self):
		for dxH, dyH in self.dirHs:
			xH, yH = self.pH
			while True:
				xH, yH = xH + dxH, yH + dyH
				if (xH, yH) not in self.grid.open:
					break
				self.grid.illuminate((xH, yH))

	def draw0(self):
		xG, yG = grid.GconvertH(self.pH)
		xV, yV = view.VconvertG((xG, yG))
		r = T(view.VscaleG * 0.3)
		h = T(view.VscaleG * 0.2)
		pygame.draw.circle(pview.screen, (240, 120, 120), (xV, yV - h), r)
		xH0, yH0 = self.pH
		for dxH, dyH in self.dirHs:
			xH, yH = self.pH
			n = 0
			while True:
				xH, yH = xH + dxH, yH + dyH
				if (xH, yH) not in self.grid.open:
					break
				n += 1
			if n > 0:
				pH0 = xH0 + dxH * 0.5, yH0 + dyH * 0.5
				pH1 = xH0 + dxH * (n + 0.5), yH0 + dyH * (n + 0.5)
				xV0, yV0 = view.VconvertG(grid.GconvertH(pH0))
				xV1, yV1 = view.VconvertG(grid.GconvertH(pH1))
				pygame.draw.line(pview.screen, (255, 160, 160),
					(xV0, yV0 - h), (xV1, yV1 - h), T(view.VscaleG * 0.1))


