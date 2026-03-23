import pygame, math
from . import view, control
from . import fuzz, pview

class Star:
	def __init__(self, pos, mag):
		self.pos = pos
		self.mag = mag

	def distanceto(self, pG):
		return math.distance(self.pos, pG)

	def draw(self):
		pV = view.VconvertG(self.pos)
		rV = pview.T(5) if self is control.cursor else pview.T(2)
		color = (255, 255, 255) if self is control.cursor else (200, 200, 200)
		pygame.draw.circle(pview.screen, color, pV, rV)


