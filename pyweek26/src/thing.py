import pygame, math, random
from . import enco, state, graphics

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

class Lifetime(enco.Component):
	def __init__(self, lifetime = 1):
		self.lifetime = lifetime
	def start(self):
		self.f = 0
	def think(self, dt):
		self.f = self.t / self.lifetime
		if self.f >= 1:
			self.alive = False

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
		self.landed = True
	def move(self, dt, dx, dy, turn, act, acthold):
		if self.landed and self.section is not None:
			self.section.move(self, dt, dx, dy, turn)
		self.pos += dt * self.v
		if act:
			if self.section.act(self):
				pass
			elif self.landed:
				self.landed = False
				self.toleap = 20
				self.v.z = 5
		if not acthold:
			self.toleap = 0
	def think(self, dt):
		if not self.landed:
			toleap = min(self.toleap, 100 * dt)
			self.toleap -= toleap
			self.v.z += toleap
			self.v.z -= 60 * dt
			if self.pos.z < self.section.pos.z:
				self.landed = True
				self.v.z = 0
				self.pos.z = self.section.pos.z
				state.effects.append(Splash(self.pos))
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

@WorldBound()
@Lives()
@Lifetime()
class Splash():
	def __init__(self, pos, lifetime=0.35):
		self.start()
		self.pos = pos * 1
		self.color = [0, 0.8, 0.8, 0.5]
		self.lifetime = lifetime
	def draw(self):
		z = self.f * (1 - self.f) * 4
		z = 0.1
		r = 2.5 * self.f
		graphics.drawcircle(self.pos + pygame.math.Vector3(0, 0, z), r, pygame.math.Vector3(0, 0, 1), self.color)
	

