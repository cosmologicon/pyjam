from OpenGL.GL import *
import math
from . import world, enco, state, graphics

class WorldBound(enco.Component):
	def init(self, spot, **kwargs):
		self.forward, self.left, self.up = spot
		self.h = 0
		self.pos = math.norm(self.up, world.R + self.h)

	def spotrot(self, axis, theta):
		self.forward, self.left, self.up = world.spotrot(axis, (self.forward, self.left, self.up), theta)

	def orient(self):
		glMultMatrixf([*self.forward,0,  *self.left,0,  *self.up,0,  0,0,0,1])
		glTranslate(0, 0, world.R + self.h)

	def relpos(self, pos):
		x, y, z = [math.dot(pos, vec) for vec in (self.forward, self.left, self.up)]
		return x, y, z - world.R # - self.h

	def step(self, d):
		if d == 0:
			return
		dA = math.tan(d / world.R)
		self.up = math.norm(world.linsum(self.up, 1, self.forward, dA))
		self.forward = math.norm(world.cross(self.left, self.up))

	def rotate(self, a):
		if a == 0:
			return
		C, S = math.CS(a)
		f0, l0 = self.forward, self.left
		self.forward = math.norm(world.linsum(f0, C, l0, S))
		self.left = math.norm(world.linsum(f0, -S, l0, C))

class Floats(enco.Component):
	def think(self, dt):
		self.h = state.tideat(self.up)

class Bobs(enco.Component):
	def __init__(self):
		self.hbob = 0
		self.bbob = 0.4
		self.vbob = 0
		self.wbob = 10

	def think(self, dt):
		abob = -self.wbob * self.hbob
		self.hbob += 0.5 * abob * dt ** 2 + self.vbob * dt
		self.vbob += abob * dt
		self.vbob *= math.exp(-self.bbob * dt)
		self.h = state.tideat(self.up) + self.hbob

class Movable(enco.Component):
	def __init__(self, b = 1, fdrag = 0.2, vmax = 100):
		self.v = 0, 0, 0
		self.b = b
		self.fdrag = fdrag
		self.vmax = vmax
		self.vground = 0, 0, 0

	def accelerate(self, a):
		self.v = world.plus(self.v, world.times(self.forward, a))
		if math.length(self.v) > self.vmax:
			self.v = math.norm(self.v, self.vmax)
		self.vbob += 0.006 * a


	def aground(self, island):
		d = min(2 - island.distout(self.up), 10)
		if d < 0:
			return 0, 0, 0
		return math.norm(world.plus(self.up, world.neg(island.up)), 5000 * d)

	def think(self, dt):
		b = self.b / math.fadebetween(abs(math.dot(self.forward, math.norm(self.v))), 0, self.fdrag, 1, 1)
		f = math.exp(-dt * b)
		self.v = world.times(self.v, f)
		ag = world.plus(*[self.aground(island) for island in state.islands])
		self.vground = world.plus(self.vground, world.times(ag, dt))
		self.vground = math.norm(self.vground, min(math.length(self.vground) * math.exp(-dt * 100), 5000))
		
		v = world.plus(self.v, self.vground)
		z = math.norm(world.cross(self.up, v))
		self.spotrot(z, math.length(v) * dt / world.R)
		self.v = world.perp(self.v, self.up)
		self.vground = world.perp(self.vground, self.up)

		self.pos = math.norm(self.up, world.R + self.h)


@WorldBound()
@Bobs()
@Movable(b = 3)
class You:
	def __init__(self):
		self.init(spot = world.spot0)

	def control(self, dt, kpressed):
		dx = kpressed["left"] - kpressed["right"]
		dy = kpressed["up"] - kpressed["down"]
		self.accelerate(1000 * dt * dy)
		self.rotate(2 * dt * dx)

@WorldBound()
@Floats()
class MoonRod:
	def __init__(self):
		self.init(spot = world.spotrot(math.norm([1, 1, 1]), world.spot0, 0.4))
		self.think(0)

	def think(self, dt):
		state.rmoon = self.up

@WorldBound()
class Island:
	def __init__(self, name, spot, ispec, R):
		self.init(spot = spot)
		self.name = name
		self.ispec = ispec
		self.R = R

	def distout(self, up):
		if math.dot(self.up, up) < 0.5:
			return world.R
		x, y, z = self.relpos(math.norm(up, world.R))
		r = math.asin(math.length([x, y]) / world.R) * world.R
		theta = math.atan2(y, x)
		isize = graphics.isize(self.ispec, theta)
		return r - self.R * isize




def init():
	state.moonrod = MoonRod()
	names = ["Apex", "Botany", "Cruz", "Xenia", "Yastreb", "Zodiac"]
	ispots = [
		(world.nzhat, world.nyhat, world.nxhat),
		(world.nxhat, world.nzhat, world.nyhat),
		(world.nyhat, world.nxhat, world.nzhat),
		(world.yhat, world.zhat, world.xhat),
		(world.zhat, world.xhat, world.yhat),
		(world.xhat, world.yhat, world.zhat),
	]
	ispecs = [
		[
			(0.10, 3, j * math.phi % 1),
			(0.07, 5, j * math.phi ** 2 % 1),
#			(0.05, 7, j * math.phi ** 3 % 1),
			(0.03, 17, j * math.phi ** 4 % 1),
			(0.02, 29, j * math.phi ** 5 % 1),
		]
		for j in range(10, 16)
	]
	Rs = [math.mix(25, 35, j * math.phi % 1) for j in range(6)]
	for name, ispot, ispec, R in zip(names, ispots, ispecs, Rs):
		graphics.renderisland(name, ispec, R)
		state.islands.append(Island(name, ispot, ispec, R))


