import pygame
from . import view, ptext, img, state
from .util import F

cursor = None
buttons = []

done = set()  # For instruction quest

class Button(object):
	def __init__(self, rect, name):
		self.rect = rect
		self.name = name
	def within(self, screenpos):
		return pygame.Rect(F(self.rect)).collidepoint(screenpos)
	def draw(self):
		rect = pygame.Rect(F(self.rect))
		if self.name.startswith("Grow"):
			text, flavor = self.name.split()
			pygame.draw.circle(view.screen, (0, 0, 0), rect.center, int(rect.width / 1.7))
			img.draw("organelle-" + flavor, rect.center, radius = int(rect.width / 1.8))
			color = "white" if state.canbuy(flavor) else "#444444"
			ptext.draw(text, color = color, shadow = (1, 1), scolor = "black",
				fontsize = F(34), center = rect.center)
		else:
			view.screen.fill((100, 50, 0), rect)
			ptext.draw(self.name, color = "white", shadow = (1, 1), scolor = "black",
				fontsize = F(18), center = rect.center)

class TowerInfo(object):
	def __init__(self):
		self.current = None
		self.target = None
		self.alpha = 0
	def think(self, dt):
		if self.target != self.current:
			if self.alpha > 0:
				self.alpha = max(0, self.alpha - 5 * dt)
			if self.alpha == 0:
				self.current = self.target
		elif self.current is not None:
			self.alpha = min(1, self.alpha + 5 * dt)
	def draw(self):
		if self.current is None:
			return
		text = self.current
		ptext.draw(text, topright = F(844, 10), fontsize = F(30),
			color = "yellow", shadow = (1, 1), alpha = self.alpha)

towerinfo = TowerInfo()



