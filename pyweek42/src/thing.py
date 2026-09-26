# Unless otherwise noted, all positions and distances in this module are game (G) coodinates.

import math, pygame
from . import pview, graphics, view, settings, geometry, enco, state
from .pview import T

class You:
	imgscale = 0.025
	def __init__(self, pos):
		self.r = 1
		self.pos = pos
		self.speed = 10
		self.Aface = 0
		self.Amove = None
		self.swing = 0
		self.twalk = 0
		self.touch = 0

	def scoot(self, dpos):
		self.pos = geometry.vecadd(self.pos, dpos)
		self.pos = state.constrain_to_room(self.pos, self.r)

	def control(self, dx, dy):
		if dx or dy:
			dx, dy = math.norm((dx, dy))
		self.vx = self.speed * dx
		self.vy = self.speed * dy
		if self.vx or self.vy:
			self.Amove = geometry.angletoward((self.vx, self.vy))
		else:
			self.Amove = None

	def think(self, dt):
		self.touch = math.approach(self.touch, 0, dt)
		dt *= state.youfactor()
		self.scoot((self.vx * dt, self.vy * dt))
		if self.Amove is not None:
			self.Aface = math.approachA(self.Aface, self.Amove, 10 * dt)
			self.twalk += dt
			self.swing = math.sin(10 * self.twalk)
		else:
			self.twalk = 0
			self.swing = math.approach(self.swing, 0, 5 * dt)

	def currentimg(self):			
		jswing = int(round(self.swing * 2))
		frame = { -2: 4, -1: 3, 0: 0, 1: 1, 2: 2 }[jswing]
		return f"walk-{frame}"

	def draw(self):
		angle = geometry.pgangle(self.Aface)
		scale = self.imgscale * self.r
		graphics.drawimgG(self.currentimg(), self.pos, scale, angle)
		if settings.DEBUG:
			graphics.drawcircleG(self.pos, self.r, (255, 200, 100))

	def hurt(self):
		if self.touch:
			return
		state.hurt()
		self.touch = 0.5

class Hazardous(enco.Component):
	def hitsyou(self, you):
		return self.intersectsyou(you)

class Stationary(enco.Component):
	def __init__(self):
		self.alive = True

	def think(self, dt):
		pass

class ConstantVelocity(enco.Component):
	def __init__(self):
		self.alive = True

	def think(self, dt):
		x, y = self.pos
		x += self.vx * dt
		y += self.vy * dt
		self.pos = x, y
		# TODO: not alive when offscreen


class Circular(enco.Component):
	imgscale = 0.011
	def __init__(self):
		self.tspin = 0

	def think(self, dt):
		self.tspin += dt

	def intersectsyou(self, you):
		return math.distance(self.pos, you.pos) < self.r + you.r

	def draw(self):
		angle = 400 * self.tspin
		graphics.drawimgG("hazard", self.pos, self.imgscale * self.r, angle = angle)
		if settings.DEBUG:
			graphics.drawcircleG(self.pos, self.r, self.color)


class Rectangular(enco.Component):
	def intersectsyou(self, you):
		return geometry.intersectrectcircle(self.pos, self.size, you.pos, you.r)

	def draw(self):
		graphics.drawrectG(self.pos, self.size, self.color)


@Hazardous()
@Stationary()
@Circular()
class CircleHazard:
	color = 255, 0, 0
	def __init__(self, pos, r):
		self.pos = pos
		self.r = r


@Hazardous()
@Stationary()
@Rectangular()
class RectangleHazard:
	color = 255, 0, 0
	def __init__(self, pos, size):
		self.pos = pos
		self.size = size

@Hazardous()
@ConstantVelocity()
@Circular()
class FlareHazard:
	color = 255, 0, 0
	def __init__(self, pos, r, vel):
		self.pos = pos
		self.r = r
		self.vx, self.vy = vel

class Lifetime(enco.Component):
	def __init__(self, T):
		self.T = T
		self.f = 0
		self.t = 0
		self.alive = True

	def think(self, dt):
		self.t = math.approach(self.t, self.T, dt)
		self.f = self.t / self.T
		self.alive = self.t < self.T

@Hazardous()
@ConstantVelocity()
@Rectangular()
class BoltHazard:
	color = 255, 0, 0
	def __init__(self, pos, size, vel):
		self.pos = pos
		self.size = size
		self.vx, self.vy = vel

@Lifetime(1)
@Circular()
class FlareSpawner:
	color = 255, 0, 0
	def __init__(self, pos, rmax, vel):
		self.pos = pos
		self.rmax = rmax
		self.vel = vel
		self.r = 0

	def spawn(self):
		flare = FlareHazard(self.pos, self.rmax, self.vel)
		flare.tspin = self.tspin
		state.hazards.append(flare)
	
	def think(self, dt):
		self.r = self.rmax * self.f
	
class Salvo:
	def __init__(self, t, flipH = False, flipV = False):
		self.alive = True
		self.t = -t
		self.spec = self.getspec()
		if flipH:
			self.spec = [(t, (-x, y), r, (-vx, vy)) for t, (x, y), r, (vx, vy) in self.spec]
		if flipV:
			self.spec = [(t, (x, -y), r, (vx, -vy)) for t, (x, y), r, (vx, vy) in self.spec]

	def think(self, dt):
		self.t += dt
		while self.spec and self.t >= self.spec[0][0]:
			t, pos, size, vel = self.spec.pop(0)
			spawner = FlareSpawner(pos, size, vel)
			state.spawners.append(spawner)
		self.alive = bool(self.spec)
		
	
class TopSalvo5(Salvo):
	def getspec(self):
		xs = [-3, 6, 0, -6, 3]
		return [(j * 0.4, (x, -8), 2, (0, 20)) for j, x in enumerate(xs)]

class SalvoEdges(Salvo):
	def getspec(self):
		return [
			(0, (-6, -8), 2, (0, 20)),
			(0, (6, 8), 2, (0, -20)),
		]


class XSalvo(Salvo):
	def getspec(self):
		dx, dy = math.norm((8, 5))
		return [
			(0, (12 * dx, -12 * dy), 1.5, (-20 * dx, 20 * dy)),
			(0, (-12 * dx, -12 * dy), 1.5, (20 * dx, 20 * dy)),
		]

class SweepSalvoR(Salvo):
	def getspec(self):
		xs = [-6, -3, 0, 3, 6]
		return [(j * 0.8, (x, -8), 1.5, (0, 20)) for j, x in enumerate(xs)]

class SweepSalvoD(Salvo):
	def getspec(self):
		ys = [-3, 0, 3]
		return [(j * 0.6, (11, y), 1.5, (-20, 0)) for j, y in enumerate(ys)]

class SalvoRLR(Salvo):
	def getspec(self):
		return [
			(0, (11, -3), 1, (-20, 0)),
			(0, (-11, 0), 1, (20, 0)),
			(0, (11, 3), 1, (-20, 0)),
		]

class MegaSalvo(Salvo):
	def getspec(self):
		return [
			(0, (11, -1.5), 3.5, (-10, 0)),
			(1.5, (11, 1.5), 3.5, (-10, 0)),
		]

class SalvoZ(Salvo):
	def getspec(self):
		return [
			(0, (11, -3), 1, (-12, 0)),
			(0.2, (11, -2), 1, (-12, 0)),
			(0.4, (11, -1), 1, (-12, 0)),
			(0.6, (11, 0), 1, (-12, 0)),
			(0.8, (11, 1), 1, (-12, 0)),
			(1.4, (11, -1), 1, (-12, 0)),
			(1.6, (11, 0), 1, (-12, 0)),
			(1.8, (11, 1), 1, (-12, 0)),
			(2.0, (11, 2), 1, (-12, 0)),
			(2.2, (11, 3), 1, (-12, 0)),
		]
	




