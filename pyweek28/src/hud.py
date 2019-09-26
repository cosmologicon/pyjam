import pygame
from . import pview, ptext
from .pview import T

class Button:
	def __init__(self, text, pV, size = (80, 80)):
		self.text = text
		self.pV = pV
		self.size = size
		self.rect0 = pygame.Rect(0, 0, *size)
		self.rect0.center = pV
		self.color = 80, 80, 80
	def getrect(self):
		return T(self.rect0)
	def draw(self):
		# TODO: cache button surfaces
		rect = self.getrect()
		pview.screen.fill(self.color, rect)
		ptext.draw(self.text, center = T(self.pV), owidth = 1, fontsize = T(32), width = rect.w)


class HUD:
	def __init__(self):
		self.buttons = [
			Button("Rotate Left", (440, 600)),
			Button("Rotate Right", (840, 600)),
		]
	def draw(self):
		for button in self.buttons:
			button.draw()

	def buttonat(self, pos):
		for button in self.buttons:
			if button.getrect().collidepoint(pos):
				return button
		return None

