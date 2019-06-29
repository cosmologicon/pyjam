from __future__ import division
import pygame
from . import settings, pview
from .pview import I

class Controls():
	def __init__(self):
		self.quit = False
		self.kdowns = set()
		self.mdown = False
		self.mup = False
		self.misdown = pygame.mouse.get_pressed()[0]
		self.mpos = I([p / pview.f for p in pygame.mouse.get_pos()])
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.quit = True
				else:
					self.kdowns.add(event.key)
					self.kdowns.add(event.unicode)
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				self.mdown = True
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				self.mup = True

	def clear(self):
		self.kdowns = set()
		self.mdown = False
		self.mup = False
		return self



