from OpenGL.GL import *
import math
from . import world, enco

class WorldBound(enco.Component):
	def init(self, spot, **kwargs):
		self.forward, self.left, self.up = spot
		self.h = 0
		self.pos = math.norm(self.up, world.R + self.h)

	def spotrot(self, axis, theta):
		self.forward, self.left, self.up = world.spotrot(axis, (self.forward, self.left, self.up), theta)

	def orient(self):
		glMultMatrixf([*self.forward,0,  *self.left,0,  *self.up,0,  0,0,0,1])

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

class Movable(enco.Component):
	def __init__(self, b = 1, fdrag = 0.2, vmax = 100):
		self.v = 0, 0, 0
		self.b = b
		self.fdrag = fdrag
		self.vmax = vmax

	def accelerate(self, a):
		self.v = world.plus(self.v, world.times(self.forward, a))
		if math.length(self.v) > self.vmax:
			self.v = math.norm(self.v, self.vmax)
	
	def think(self, dt):
		b = self.b / math.fadebetween(abs(math.dot(self.forward, math.norm(self.v))), 0, self.fdrag, 1, 1)
		f = math.exp(-dt * b)
		self.v = world.times(self.v, f)
		z = math.norm(world.cross(self.up, self.v))
		self.spotrot(z, math.length(self.v) * dt / world.R)
		proj = world.times(self.up, math.dot(self.up, self.v))
		self.v = world.plus(self.v, world.neg(proj))

		self.pos = math.norm(self.up, world.R + self.h)


@WorldBound()
@Movable(b = 3)
class You:
	def __init__(self):
		self.init(spot = world.spot0)

	def control(self, dt, kpressed):
		dx = kpressed["left"] - kpressed["right"]
		dy = kpressed["up"] - kpressed["down"]
		self.accelerate(1000 * dt * dy)
		self.rotate(2 * dt * dx)




