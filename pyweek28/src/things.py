# Game entities

from __future__ import division
import pygame, random, math
from . import pview, view, quest
from .pview import T


# TODO(Christopher): there are much better looking options than this. Revisit this once we have an
# idea for the art style.

# For now, as a placeholder, stations are represented as a collection of cylinders, and we don't do
# any fancy occlusion, we just draw them in order from the back to the front.
def randomstationpiece():
	xW = random.uniform(-1, 1)
	yW = random.uniform(-1, 1)
	xW, yW = math.norm((xW, yW), 1.2)
	zW = random.uniform(-0.4, 0.4)
	h = random.uniform(0.01, 1) ** 0.5  # Bias toward shorter cylinders
	r = math.clamp(0.5 / h, 0.1, 2)
	color = random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)
	return (xW, yW, zW), h, r, color


class Station:
	def __init__(self, name, yG):
		self.name = name
		self.yG = yG
		self.messages = []
		self.drawdata = [randomstationpiece() for _ in range(20)]
		self.quests = []
	def addquest(self, questname):
		self.quests.append(questname)
	def startquest(self, questname):
		self.quests.remove(questname)
		quest.start(questname)
	def think(self, dt):
		pass
	def draw(self, back):
		# TODO: abort early if the entire station is off screen.
		data = [(view.worldtogame(pW), h, w, color) for pW, h, w, color in self.drawdata]
		# Sort by depth
		data.sort(key = lambda entry: entry[0][1])
		for ((xG, yG), dG), h, r, color in data:
			if (back and dG > 0) or (not back and dG < 0):
				continue
			xV0, yV0 = view.gametoview((xG - r, self.yG + yG + h))
			xV1, yV1 = view.gametoview((xG + r, self.yG + yG - h))
			rect = pygame.Rect(xV0, yV0, xV1 - xV0, yV1 - yV0)
			if pview.rect.colliderect(rect):
				pview.screen.fill(color, rect)
		
