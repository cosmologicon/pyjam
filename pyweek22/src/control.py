import pygame
from . import view, ptext
from .util import F

cursor = None
buttons = []

class Button(object):
	def __init__(self, rect, name):
		self.rect = rect
		self.name = name
	def within(self, screenpos):
		return pygame.Rect(F(self.rect)).collidepoint(screenpos)
	def draw(self):
		rect = pygame.Rect(F(self.rect))
		view.screen.fill((100, 50, 0), rect)
		ptext.draw(self.name, color = "white", shadow = (1, 1), scolor = "black",
			fontsize = F(18), center = rect.center)

