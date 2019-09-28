import pygame, math
from functools import lru_cache
from . import pview, ptext
from .pview import T

@lru_cache(1000)
def buttonimg(text, w, h, fontsize):
	surf = pygame.Surface((w, h)).convert_alpha()
	surf.fill((100, 255, 255, 70))
	rect = pygame.Rect((0, 0, w, h))
	rect.inflate_ip(-w // 12, -w // 12)
	surf.fill((100, 255, 255, 50), rect)
	if text == "Rotate Left":
		def pos(x, y):
			return math.imix(0, w, x), math.imix(0, h, y)
		# TODO: draw it in inkscape
		pygame.draw.polygon(surf, (100, 255, 255), [pos(x, y) for x, y in [(0.65, 0.2), (0.65, 0.8), (0.3, 0.5)]])
		pygame.draw.polygon(surf, (100, 255, 255, 100), [pos(x, y) for x, y in [(0.6, 0.3), (0.6, 0.7), (0.35, 0.5)]])
	elif text == "Rotate Right":
		return pygame.transform.flip(buttonimg("Rotate Left", w, h, fontsize), True, False)
	else:
		ptext.draw(text, surf = surf, center = rect.center, fontsize = fontsize, owidth = 1, color = (100, 255, 255), width = rect.w)
	return surf



class Button:
	def __init__(self, text, pV, size = (80, 80), isvisible = None):
		self.text = text
		self.pV = pV
		self.size = size
		self.rect0 = pygame.Rect(0, 0, *size)
		self.rect0.center = pV
		self.color = 80, 80, 80
		self.isvisible = isvisible or (lambda: True)
	def getrect(self):
		return T(self.rect0)
	def draw(self):
		w, h = self.size
		surf = buttonimg(self.text, T(w), T(h), T(32))
		pview.screen.blit(surf, surf.get_rect(center = T(self.pV)))


class HUD:
	def __init__(self):
		self.buttons = [
		]
	def draw(self):
		for button in self.buttons:
			if button.isvisible():
				button.draw()

	def buttonat(self, pos):
		for button in self.buttons:
			if button.isvisible() and button.getrect().collidepoint(pos):
				return button
		return None

