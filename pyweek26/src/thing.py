import pygame, math, random
from OpenGL.GL import *
from . import enco, state, graphics, settings

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
		self.tjump = 0
	def move(self, dt, dx, dy, turn, act, acthold):
		if self.landed and self.section is not None:
			self.section.move(self, dt, dx, dy, turn)
		self.pos += dt * self.v
		if act:
			if self.section.act(self):
				pass
			elif self.landed:  # Jump
				self.landed = False
				self.toleap = 20
				self.v.z = 5
			elif self.tjump < 0.4:  # Dive
				self.toleap = 0
				self.v.z = -40
		if not acthold:
			self.toleap = 0
	def think(self, dt):
		dz = self.section.dzwater(self.pos)
		if self.landed:
			# Damped constant-force motion to settle
			self.v.z -= 60 * dz * dt
			self.v.z *= math.exp(-0.4 * dt)
			self.tjump = 0
		else:
			self.tjump += dt
			toleap = min(self.toleap, 100 * dt)
			self.toleap -= toleap
			self.v.z += toleap
			self.v.z -= 60 * dt
			if dz < 0 and self.v.z < 0:
				self.landed = True
#				self.v.z = 0
#				self.pos.z = self.section.pos.z
				state.effects.append(Splash(self.pos))
		# Swim faster if you're going forward.
		v = self.v.length()
		f = math.smoothfadebetween(v, 0, 0.5, 20, 3)
		self.Tswim += dt * f
	# Up/down angle for the purpose of rendering
	def rangle(self):
		vz = self.v.z
		if self.landed:
			p = 1 * self.pos
			dp = p + self.v
			p.z = 0
			dp.z = 0
			vz += self.section.dzwater(dp) - self.section.dzwater(p)
		return math.degrees(math.atan(vz / 20))

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

# Note: this class is only here for debug graphics. You can get the same information from
# pool.drainers.
@WorldBound()
@WaterBound(fixed = True)
@Lives()
class Waterfall():
	def __init__(self, top, bottom):
		self.start()
		self.top = 1 * top.pos
		self.top.z -= 3
		self.bottom = 1 * self.top
		self.bottom.z = bottom.pos.z
		self.section = bottom
		self.pos = self.bottom
		self.h = self.top.z - self.bottom.z
	def think(self, dt):
		pass
	def draw(self):
		if not settings.debug_graphics:
			return
		graphics.drawcylinder(self.pos, 1, self.h, (0, 0, 0.3, 1))


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

# Just needed for debug graphics.
@WorldBound()
@WaterBound(fixed = True)
@Lives()
class Tentacles():
	def __init__(self, pool):
		self.start()
		self.pos = pool.pos * 1
	def draw(self):
		if not settings.debug_graphics:
			return
		glPushMatrix()
		glTranslate(*self.pos)
		for jtheta in range(5):
			glPushMatrix()
			tilt = math.mix(10, 70, math.cycle(jtheta / 5 + self.t / 5))
			glRotate(jtheta * 360 * 2 / 5, 0, 0, 1)
			glRotate(tilt, 1, 0, 0)
			graphics.drawcone((0, 0, 0), 2, 12, (1, 0, 0.5, 1))
			glPopMatrix()
		glPopMatrix()
	

