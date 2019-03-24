import pygame, math
from . import enco, ptext, pview
from .pview import T

class Coin():
	def __init__(self, pos, value):
		self.r = 60
		self.pos = pos
		self.value = value
		self.color = pygame.Color("orange")

	def collide(self, point):
		return math.distance(self.pos, point) < self.r

	def draw(self):
		pygame.draw.circle(pview.screen, self.color, T(self.pos), T(self.r))
		pygame.draw.circle(pview.screen, pygame.Color("black"), T(self.pos), T(self.r + 2), T(4))
		ptext.draw("%d" % self.value, center = T(self.pos), fontsize = T(2 * self.r), owidth = 1)

	def highlight(self):
		pygame.draw.circle(pview.screen, pygame.Color("red"), T(self.pos), T(self.r + 8), T(4))


