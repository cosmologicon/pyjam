import pygame, math, random
from . import enco

class WorldBound(enco.Component):
	def start(self):
		self.pos = pygame.math.Vector3(0, 0, 0)

class WaterBound(enco.Component):
	def start(self):
		self.section = None
	def flow(self, dt):
		if self.section is not None:
			self.section.flow(dt, self)

class Lives(enco.Component):
	def start(self):
		self.t = 0
	def think(self, dt):
		self.t += dt

class Faces(enco.Component):
	def start(self):
		self.heading = 0
		self.face = pygame.math.Vector3(0, 1, 0)
	def think(self, dt):
		self.face = pygame.math.Vector3(math.sin(self.heading), math.cos(self.heading), 0)

class MovesWithArrows(enco.Component):
	def start(self):
		self.v = pygame.math.Vector3(0, 0, 0)
		self.Tswim = 0  # Animation timer for swimming
		self.upstream = True
	def move(self, dt, dx, dy, turn):
		if self.section is not None:
			self.section.move(self, dt, dx, dy, turn)
		self.pos += dt * self.v
	def think(self, dt):
		# Swim faster if you're going forward.
		v = self.v.length()
		f = math.smoothfadebetween(v, 0, 0.5, 20, 3)
		self.Tswim += dt * f
#		heading = 0 if self.upstream else math.tau / 2
#		self.heading = math.anglesoftapproach(self.heading, heading, 10 * dt, dymin = 0.01)
		

@WorldBound()
@WaterBound()
@Lives()
@Faces()
@MovesWithArrows()
class You():
	def __init__(self):
		self.start()

@WorldBound()
@WaterBound()
@Lives()
class Debris():
	def __init__(self):
		self.start()
		self.color = [random.uniform(0.2, 0.4) for _ in "rgb"]
		self.r = random.uniform(0.7, 1.5)
	def think(self, dt):
		pass

