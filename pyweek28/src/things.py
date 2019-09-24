# Game entities

from __future__ import division
import pygame, random, math
from . import pview, view, quest, state
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


class Car:
	def __init__(self, yG, A):
		self.yG = yG
		self.A = A
		self.n = 0  # number of passengers carried
		self.capacity = 1
		self.targetyG = self.yG
		self.vyG = 0
		self.r = 0.8
		self.R = 1.3  # Distance from central axis
		# When a car nears its destination it switches to approach mode, which is exponential braking.
		self.braking = True
	def arrived(self):
		return self.targetyG == self.yG
	def worldpos(self):
		yW, xW = math.CS(self.A * math.tau, self.R)
		zW = self.yG
		return xW, yW, zW
	def think(self, dt):
		if not self.arrived():
			b = 4  # braking factor. Set higher for shorter stops.
			brakeyG = math.softapproach(self.yG, self.targetyG, b * dt, dymin = 0.01)
			if not self.braking:
				self.vyG += 200 * dt
				goyG = math.approach(self.yG, self.targetyG, self.vyG * dt)
				if abs(self.yG - brakeyG) < abs(self.yG - goyG):
					self.braking = True
				else:
					self.yG = goyG
			if self.braking:
				self.vyG = abs(brakeyG - self.yG) / dt
				self.yG = brakeyG
		# TODO: remove. This is just for demo purposes to make it seem more dynamic.
		if self.arrived():
			self.settarget(random.choice(state.stations).yG)
	def settarget(self, yG):
		self.targetyG = yG
		self.braking = False
	def draw(self, back):
		# TODO: abort early if the entire car is off screen.
		(xG, yG), dG = view.worldtogame(self.worldpos())
		if (back and dG > 0) or (not back and dG < 0):
			return
		h = 0.5
		color = 200, 100, 100
		xV0, yV0 = view.gametoview((xG - self.r, yG + h))
		xV1, yV1 = view.gametoview((xG + self.r, yG - h))
		rect = pygame.Rect(xV0, yV0, xV1 - xV0, yV1 - yV0)
		if pview.rect.colliderect(rect):
			pview.screen.fill(color, rect)

