from OpenGL.GL import *
import math
from . import world, enco, state, graphics, quest


class Lifetime(enco.Component):
	def __init__(self, lifetime):
		self.lifetime = lifetime
		self.t = 0
		self.f = 0
		self.alive = True
	def think(self, dt):
		self.t += dt
		self.f = math.clamp(self.t / self.lifetime, 0, 1)
		self.alive = self.t < self.lifetime

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
		self.vecho = 0, 0, 0

	def accelerate(self, a):
		self.v = world.plus(self.v, world.times(self.forward, a))
		if math.length(self.v) > self.vmax:
			self.v = math.norm(self.v, self.vmax)
		self.vbob += 0.006 * a


	def aground(self, island):
		d = min(3 - island.distout(self.up), 10)
		if d < 0:
			return 0, 0, 0
		return math.norm(world.plus(self.up, world.neg(island.up)), 5000 * d)

	def getfullv(self):
		return world.plus(self.v, self.vground)


	def think(self, dt):
		b = self.b / math.fadebetween(abs(math.dot(self.forward, math.norm(self.v))), 0, self.fdrag, 1, 1)
		f = math.exp(-dt * b)
		self.v = world.times(self.v, f)

		ag = world.plus(*[self.aground(island) for island in state.islands])
		self.vground = world.plus(self.vground, world.times(ag, dt))
		self.vground = math.norm(self.vground, min(math.length(self.vground) * math.exp(-dt * 100), 5000))

		v = self.getfullv()
		self.vecho = math.mix(self.vecho, v, 1 - math.exp(-dt * 10))

		z = math.norm(world.cross(self.up, v))
		self.spotrot(z, math.length(v) * dt / world.R)
		self.v = world.perp(self.v, self.up)
		self.vground = world.perp(self.vground, self.up)

		self.pos = math.norm(self.up, world.R + self.h)

class AnchorSlow(enco.Component):
	def think(self, dt):
		vmax = 100 if state.anchored is None else 40
		self.vmax = math.approach(self.vmax, vmax, 100 * dt)

class Anchorable(enco.Component):
	def init(self, **kwargs):
		self.anchor = None
		self.arange = 8
	def think(self, dt):
		if self.anchor is not None:
			amax = self.arange / world.R
			a = math.length(world.plus(self.up, world.neg(self.anchor.up)))
			if a > amax:
				self.spotrot(math.norm(world.cross(self.up, self.anchor.up)), a - amax)
			
	def anchorableto(self, obj):
		d = world.R * math.length(world.plus(self.up, world.neg(obj.up)))
		return d < self.arange
	
	def anchorto(self, obj):
		self.anchor = obj
	
	def unanchor(self):
		self.anchor = None

class SpawnsSplash(enco.Component):
	def init(self, **kwargs):
		self.tsplash = 0
		self.splashtime = 0.05
	def think(self, dt):
		self.tsplash += dt
		while self.tsplash > self.splashtime:
			self.tsplash -= self.splashtime
			self.spawnsplash()
	def spawnsplash(self):
		v = self.vecho
		if math.length(v) < 60:
			return
		spot = self.forward, self.left, self.up
		state.effects.append(Splash(spot, v))


@WorldBound()
@Bobs()
@Movable(b = 3)
@SpawnsSplash()
@AnchorSlow()
class You:
	def __init__(self, spot):
		self.init(spot = spot)

	def control(self, dt, kpressed):
		dx = kpressed["left"] - kpressed["right"]
		dy = kpressed["up"] - kpressed["down"]
		self.accelerate(1000 * dt * dy)
		self.rotate(2 * dt * dx)

@WorldBound()
@Anchorable()
@Floats()
class Moonrod:
	def __init__(self, spot):
		self.init(spot = spot)
		self.think(0)

	def think(self, dt):
		state.rmoon = self.up

@WorldBound()
class Disc:
	def __init__(self, spot, color):
		self.init(spot = spot)
		self.color = color
		self.t = 0
		self.h = -4.8
		self.alive = True

	def think(self, dt):
		self.t += dt

	def draw(self):
		dh = state.tideat(self.up) - self.h
		if dh > 0:
			dx = 0.2 * dh * graphics.noiseat([0.5, 0.5, self.t], [2, 1.2, 0.7], seed=self.color)
			dy = 0.2 * dh * graphics.noiseat([4.5, 4.5, self.t], [2, 1.2, 0.7], seed=self.color)
			da = 0.2 * dh * graphics.noiseat([0.5, 4.5, self.t], [2, 1.2, 0.7], seed=self.color)
			db = 0.2 * dh * graphics.noiseat([4.5, 0.5, self.t], [2, 1.2, 0.7], seed=self.color)
			theta = math.degrees(math.atan2(da, db))
			s = 1 + 0.02 * math.length([da, db])
			glRotatef(theta, 0, 0, 1)
			glScale(s, 1/s, 1)
			glRotatef(-theta, 0, 0, 1)
			glTranslatef(dx, dy, 0)
		alpha = math.fadebetween(self.t, 0, 0, 6, 1)
		if alpha < 1:
			glEnable(GL_BLEND)
			glBlendColor(0, 0, 0, alpha)
			glBlendFunc(GL_CONSTANT_ALPHA, GL_ONE_MINUS_CONSTANT_ALPHA)

		glCallList(graphics.lists.discs[self.color][0])
		glRotatef(100 * self.t % 360, 0, 0, 1)
		glCallList(graphics.lists.discs[self.color][1])
		glRotatef(-100 * math.phi * self.t % 360, 0, 0, 1)
		glCallList(graphics.lists.discs[self.color][2])
		if alpha < 1:
			glDisable(GL_BLEND)

	def udraw(self):
		glTranslatef(0, 0, 0.01)
		self.draw()

	def adraw(self):
		glCallList(graphics.lists.discs[self.color][3])

	def touched(self):
		d = world.R * math.distance(self.up, state.you.up)
		v = math.length(state.you.vecho)
		return d < 14 and v < 1 and state.tideat(self.up) < self.h + 1


@WorldBound()
class Island:
	def __init__(self, name, spot, ispec, R):
		self.init(spot = spot)
		self.name = name
		self.ispec = ispec
		self.R = R
		self.ztree = 0
		self.ktree = 0
		self.tgrow = 0
		self.tbloom = 0
		self.grown = False
		self.bloomed = False

	def distout(self, up):
		if math.dot(self.up, up) < 0.5:
			return world.R
		x, y, z = self.relpos(math.norm(up, world.R))
		r = math.asin(math.length([x, y]) / world.R) * world.R
		theta = math.atan2(y, x)
		isize = graphics.isize(self.ispec, theta)
		z = state.tideat(up)
		isize *= graphics.isr(z)
		return r - isize * self.R / 25

	def draw(self):
		glCallList(graphics.lists.islands[self.name])
		# k = (0.3 * 0.001 * pygame.time.get_ticks()) % 1
		glTranslatef(0, 0, -30 * (1 - self.ztree))
		glRotatef(100 * (1 - self.ztree), 0, 0, 1)
		graphics.rendertree(self.ktree)

	def think(self, dt):
		if self.grown:
			self.tgrow += dt
			self.ztree = math.softapproach(self.ztree, 1, 2 * dt, dymin = 0.001)
		if self.bloomed:
			self.tbloom += dt
			self.ktree = 1 - math.cos(5 * self.tbloom) * math.exp(-1 * self.tbloom)
			if self.tbloom > 10:
				self.ktree = 1

	def grow(self):
		if self.grown:
			return
		self.grown = True
	
	def bloom(self):
		if self.bloomed:
			return
		self.bloomed = True

@Lifetime(1)
@WorldBound()
class Splash:
	def __init__(self, spot, v):
		self.init(spot = spot)
		self.ospot = world.randomspot()
		self.v = v
		self.fsplash = math.fadebetween(math.length(v), 0, 0.3, 60, 1)
		self.lifetime = 0.4 * self.fsplash
		self.h = 0
		self.move(0.02)
	def move(self, dt):
		self.spotrot(math.norm(world.cross(self.up, self.v)), math.length(self.v) * dt / world.R)
	def think(self, dt):
		v = state.you.getfullv()
		self.v = math.mix(self.v, v, 1 - math.exp(-dt * 6))
		
		self.h = 1 + 6 * self.fsplash * self.f * (1 - self.f)
		self.move(dt)
		if not self.alive:
			quest.pourwater(self.up)
	def draw(self):
		f, l, u = self.ospot
		glMultMatrixf([*f,0,  *l,0,  *u,0,  0,0,0,1])
		s = math.mix(0.3, 1, self.fsplash) * math.mix(0.3, 1, self.f) * 14
		glScale(s, s, s)
		glCallList(graphics.lists.splash)
#		glCallList(graphics.lists.wake)

@WorldBound()
class Seed:
	def __init__(self, island0):
		spot = island0.forward, island0.left, island0.up
		self.init(spot = spot)
		self.island0 = island0
		self.island1 = None
		self.ffollow = 0
		self.taking = True
		self.h = 10
		self.alive = True
		self.autodrop = True
		self.tgrow = 0
	def dropto(self, iname):
		if self.island1 is not None:
			return
		self.island1 = iname
		self.taking = False
		
	def grow(self, dt):
		self.tgrow += dt
		self.island1.ztree = math.fadebetween(self.tgrow, 0, 0, 1.5, 1)
		if self.island1.ztree == 1:
			self.alive = False

	def think(self, dt):
		ffollow = 1 if self.taking else 0
		self.ffollow = math.approach(self.ffollow, ffollow, dt)
		if self.ffollow == 0 and not self.taking:
			self.grow(dt)
		a = min(self.ffollow, 1 - self.ffollow) * 2
		h0 = 5 if self.ffollow > 0.5 else (25 if self.taking else 0)
		h1 = 5
		self.h = math.mix(h0, h1, a) + a * (1 - a) * 20
		you = state.you
		if self.ffollow == 1:
			self.forward, self.left, self.up = you.forward, you.left, you.up
		else:
			island = self.island1 or self.island0
			spot = (
				math.mix(island.forward, you.forward, self.ffollow),
				math.mix(island.left, you.left, self.ffollow),
				math.mix(island.up, you.up, self.ffollow),
			)
			self.forward, self.left, self.up = world.renorm(spot)
		if self.autodrop and self.island1 is None:
			iname = state.iname()
			if iname is not None:
				island = state.getisland(iname)
				if island.ztree == 0:
					self.dropto(island)
			
	def draw(self):
		glCallList(graphics.lists.seed)


def init():
	state.you = You(world.oct0)
	state.moonrod = None
	if False:
		state.moonrod = Moonrod(spot = world.oct0)
		state.moonrod.h = 5
		state.tide = 5

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

#	state.getisland("Zodiac").ktree = 1

