# Game entities

from __future__ import division
import pygame, random, math
from . import pview, view, quest, state, draw
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
	def __init__(self, name, z):
		self.name = name
		self.z = z
		self.messages = []
		self.drawdata = [randomstationpiece() for _ in range(20)]
		self.quests = []
		self.t = 0
	def addquest(self, questname):
		self.quests.append(questname)
	def startquest(self, questname):
		self.quests.remove(questname)
		quest.start(questname)
	def think(self, dt):
		self.t += dt
	def draw(self, back):
		# TODO: abort early if the entire station is off screen.
		if back:
			return
		dA = 0.1 * self.t
		draw.drawelement("gray", 0, self.z - 2, self.z - 0.7, 2, 4.2, 8, view.A, 10)
		draw.drawelement("hatch", 0, self.z - 0.7, self.z - 0.5, 4.2, 4.2, 1, view.A - 0 * dA, 100)
		draw.drawelement("window", 0, self.z - 0.5, self.z + 0.5, 4, 4, 1, view.A + dA, 20)
		draw.drawelement("hatch", 0, self.z + 0.5, self.z + 0.7, 4.2, 4.2, 1, view.A - 0 * dA, 100)
		draw.drawelement("gray", 0, self.z + 0.7, self.z + 1.4, 4.2, 2, 8, view.A, 10)

# TODO: reconsider the convention of A being the side of the cable it's on, rather than the side of
# the cable it's facing.

class Car:
	def __init__(self, z, A):
		self.z = z
		self.A = A
		self.n = 0  # number of passengers carried
		self.capacity = 1
		self.targetz = self.z
		self.vz = 0
		self.r = 0.8
		self.R = 1.3  # Distance from central axis
		# When a car nears its destination it switches to approach mode, which is exponential braking.
		self.braking = True
	def arrived(self):
		return self.targetz == self.z
	def worldpos(self):
		yW, xW = math.CS(self.A/8 * math.tau, self.R)
		return xW, yW, self.z
	def think(self, dt):
		if not self.arrived():
			b = 4  # braking factor. Set higher for shorter stops.
			brakez = math.softapproach(self.z, self.targetz, b * dt, dymin = 0.01)
			if not self.braking:
				self.vz += 200 * dt
				goz = math.approach(self.z, self.targetz, self.vz * dt)
				if abs(self.z - brakez) < abs(self.z - goz):
					self.braking = True
				else:
					self.z = goz
			if self.braking:
				self.vz = abs(brakez - self.z) / dt
				self.z = brakez
		# Move to another station once you arrive.
		# TODO: remove. This is just for demo purposes to make it seem more dynamic.
		if self.arrived():
			self.settarget(random.choice(state.stations).z)
	def settarget(self, zW):
		self.targetz = zW
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

