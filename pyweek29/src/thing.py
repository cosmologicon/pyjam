import pygame
from . import view, pview
from .pview import T


class You:
	def __init__(self):
		self.x, self.y = 0, 0
	def control(self, kdowns):
		if pygame.K_RIGHT in kdowns:
			self.x += 1
		if pygame.K_LEFT in kdowns:
			self.x -= 1
		if pygame.K_UP in kdowns:
			self.y += 1
		if pygame.K_DOWN in kdowns:
			self.y -= 1
	def think(self, dt):
		pass
	def draw(self):
		pos = view.worldtoscreen((self.x + 0.5, self.y + 0.5))
		r = T(0.25 * view.zoom)
		pygame.draw.circle(pview.screen, (200, 180, 40), pos, r, T(4))

