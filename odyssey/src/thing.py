from __future__ import division
import pygame, math, random
from pygame.math import Vector3
from OpenGL.GL import *
from . import enco, state, graphics, settings, sound

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


class TakesHit(enco.Component):
	def start(self):
		self.thurt = 0
	def stunned(self):
		return self.thurt > 0.5
	def invulnerable(self):
		return self.thurt > 0
	def think(self, dt):
		self.thurt = max(self.thurt - dt, 0)
	def pickvector(self):
		self.uspin = Vector3(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
		self.uspin = self.uspin.normalize() if self.uspin.length() else Vector3(0, 0, 1)

class Collides(enco.Component):
	def __init__(self, r = 1):
		self.r = r
	def collides(self, obj):
		d = obj.pos - self.pos
		return d.length() < self.r + obj.r

class BossKnocks(enco.Component):
	def hit(self, you):
		d = you.pos - self.pos
		if d.length() == 0:
			d = Vector3(1, 0, 0)
		if not you.invulnerable():
			you.thurt = 1
		you.vwater += 12 * d.normalize() + Vector3(0, 0, 10)
		you.landed = False
		you.pickvector()

class Knocks(enco.Component):
	def hit(self, you):
		d = you.pos - self.pos
		if d.length() == 0:
			d = Vector3(1, 0, 0)
		if not you.invulnerable():
			you.thurt = 1
		you.vwater += 5 * d.normalize()
		you.pickvector()


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
		# Confusing but this is your speed with respect to the water, not the speed of the water.
		self.vwater = pygame.math.Vector3(0, 0, 0)
		self.draining = False
	def move(self, dt, dx, dy, turn, act, acthold):
		if self.landed and not self.draining and self.section is not None:
			self.section.move(self, dt, dx, dy, turn)
		self.pos += dt * (self.v + self.vwater)
		if act and not self.draining:
			if self.section.act(self):
				pass
			elif self.landed:  # Jump
				self.landed = False
				self.toleap = 20
				self.vwater.z = 5
			elif self.tjump < 0.4:  # Dive
				self.toleap = 0
				self.vwater.z = -40
		if not acthold:
			self.toleap = 0
	def startdrain(self):
		self.draining = True
		self.tdrain = 0
		self.draintheta = 0
		self.drainsink = 0
	def movedrain(self, dt):
		dr = 5 * self.tdrain * dt
		dl = 10 * dt
		ax, ay, az = self.pos - self.section.pos
		r = math.sqrt(ax ** 2 + ay ** 2)
		dtheta = -dl / max(r, 0.5)
		r = max(r - dr, 0)
		if r > 0.01:
			theta = math.atan2(ay, ax)
			theta += dtheta
		else:
			theta = 0
		ax, ay = math.CS(theta, r)
		self.pos.x = self.section.pos.x + ax
		self.pos.y = self.section.pos.y + ay
		self.draintheta -= dtheta
		if r < 0.1:
			self.drainsink += dt
			if self.drainsink > 0.1:
				self.pos.z -= 20 * dt * (self.drainsink - 0.5) ** 2
				if self.section.dzwater(self.pos) < -2:
					self.section.drop(self)
					self.draining = False
	def think(self, dt):
		dz = self.section.dzwater(self.pos)
		if self.draining:
			self.tdrain += dt
			self.movedrain(dt)
			self.vwater *= 0
			self.v *= 0
		elif self.landed:
			# Damped constant-force motion to settle
			self.vwater.z -= 50 * dz * dt
			self.vwater *= math.exp(-2 * dt)
			self.tjump = 0
		else:
			self.tjump += dt
			toleap = min(self.toleap, 100 * dt)
			self.toleap -= toleap
			self.vwater.z += toleap
			self.vwater.z -= 60 * dt
			if dz < 0 and self.vwater.z < 0:
				sound.manager.PlaySound('splash%03d'%(random.randint(1,3)))
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
		if self.draining:
			return math.clamp(40 * self.tdrain + 100 * self.drainsink, 0, 70)
		vz = (self.v + self.vwater).z
		if self.landed:
			p = 1 * self.pos
			dp = p + self.v + self.vwater
			p.z = 0
			dp.z = 0
			vz += self.section.dzwater(dp) - self.section.dzwater(p)
		return math.degrees(math.atan(vz / 20))
	# Altitude adjustment while draining
	def drainangle(self):
		if not self.draining:
			return 0
		return math.smoothfadebetween(self.tdrain, 0.2, 0, 1.5, 30)

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
@TakesHit()
@MovesWithArrows()
class You():
	def __init__(self):
		self.r = 0.6
		self.start()

@WorldBound()
@WaterBound(fixed = True)
@SinksInPool()
@Collides()
@Knocks()
@Lives()
class Debris():
	def __init__(self, pos, section):
		self.start()
		self.pos = pos
		self.section = section
		self.color = [random.uniform(0.6, 0.8), random.uniform(0, 0.1), random.uniform(0, 0.5)]
		self.r = random.uniform(0.7, 1.5)
	def think(self, dt):
		pass
	def draw(self):
		graphics.drawobj(self)

@WorldBound()
@WaterBound(fixed = True)
@Collides()
@Knocks()
@Lives()
class Column():
	def __init__(self, pos, section):
		self.start()
		self.color = [random.uniform(0.3, 0.4) for _ in "rgb"]
		self.r = random.uniform(0.7, 1.5)
		self.section = section
	def think(self, dt):
		pass
	def draw(self):
		if not settings.debug_graphics:
			return
		graphics.drawcylinder(self.pos, 1, self.h, (0, 0, 0.3, 1))

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
@WaterBound(fixed = True)
@Collides(3)
@BossKnocks()
@Lives()
class BossHitbox():
	def __init__(self, section):
		self.start()
		self.section = section
		self.pos = self.section.pos
	def think(self, dt):
		pass
	def draw(self):
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
		self.pool = pool
		self.pos = pool.pos * 1
		
		# turn these on to set final boss animations
		state.animation.stalker.append(graphics.Stalker(pool.pos,pool))

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
	

