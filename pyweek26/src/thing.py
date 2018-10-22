import pygame, math, random
from . import enco

class WorldBound(enco.Component):
	def start(self):
		self.pos = pygame.math.Vector3(0, 0, 0)
		self.alive = True

class WaterBound(enco.Component):
	def __init__(self, fixed = False):
		self.fixed = fixed
	def start(self):
		self.section = None
	def flow(self, dt):
		if not self.fixed and self.section is not None:
			self.section.flow(dt, self)
			self.section.handoff(self)
			self.section.constrain(self)

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

class SinksInPool(enco.Component):
	def think(self, dt):
		from . import section
		if isinstance(self.section, section.Pool):
			self.pos.z -= 1 * dt
			if self.pos.z < -self.r:
				self.alive = False

@WorldBound()
@WaterBound()
@Lives()
@Faces()
@MovesWithArrows()
class You():
	def __init__(self):
		self.r = 0.6
		self.start()

@WorldBound()
@WaterBound()
@SinksInPool()
@Lives()
class Debris():
	def __init__(self):
		self.start()
		self.color = [random.uniform(0.2, 0.4) for _ in "rgb"]
		self.r = random.uniform(0.7, 1.5)
	def think(self, dt):
		pass

@WorldBound()
@WaterBound(fixed = True)
@Lives()
class SolidGrate():
	def __init__(self, section, afactor):
		self.start()
		self.section = section
		self.section.blockers.append(self)
		self.afactor = afactor
	def think(self, dt):
		pass

