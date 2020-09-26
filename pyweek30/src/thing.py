from OpenGL.GL import *
import math, random
from . import world, enco, state, graphics, sound


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

	def getspot(self):
		return self.forward, self.left, self.up

	def spotrot(self, axis, theta):
		self.forward, self.left, self.up = world.spotrot(axis, self.getspot(), theta)

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

	def orient(self):
		theta = math.fadebetween(math.dot(self.vecho, self.forward), -100, -20, 100, 20)
		glRotatef(-theta, 0, 1, 0)
		theta = math.fadebetween(math.dot(self.vecho, self.left), -10, -15, 10, 15)
		glRotatef(theta, 1, 0, 0)

class AnchorSlow(enco.Component):
	def think(self, dt):
		vmax = 100 if state.anchored is None else 40
		self.vmax = math.approach(self.vmax, vmax, 100 * dt)

class Anchorable(enco.Component):
	def init(self, **kwargs):
		self.anchor = None
		self.arange = 25
		self.dsplash = 0

	def think(self, dt):
		if self.anchor is not None:
			amax = self.arange / world.R
			a = math.length(world.plus(self.up, world.neg(self.anchor.up)))
			if a > amax:
				u = self.up
				self.spotrot(math.norm(world.cross(self.up, self.anchor.up)), a - amax)
				self.dsplash += world.R * math.distance(self.up, u)
		while self.dsplash > 1:
			state.effects.append(Splash(self.getspot(), [0, 0, 0], fsplash = 1))
			self.dsplash -= 1

			
	def anchorableto(self, obj):
		d = world.R * math.length(world.plus(self.up, world.neg(obj.up)))
		return d < self.arange
	
	def anchorto(self, obj):
		self.anchor = obj
		sound.play("attach")
	
	def unanchor(self):
		self.anchor = None
		sound.play("detach")


class Unanchorable(enco.Component):
	def init(self, **kwargs):
		self.anchor = None
		self.arange = 8
	def anchorableto(self, obj):
		return False


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
		self.h = 0

	def think(self, dt):
		state.rmoon = self.up

	def drawmoon(self):
		glTranslatef(0, 0, 20)
		glScalef(5, 5, 5)
		glCallList(graphics.lists.moon)
		


@WorldBound()
@Anchorable()
@Floats()
class Windrod:
	def __init__(self, spot):
		self.init(spot = spot)
		self.t = 0
		self.twind = 0
		self.think(0)
		self.h = 0

	def think(self, dt):
		self.t += dt
		self.twind += dt * math.fadebetween(self.t, 0, 0, 10, 1)
		state.rmoon = world.rot(self.up, self.left, 1 * self.twind)

	def drawmoon(self):
		C, S = math.CS(1 * self.twind)
		glTranslatef(-10 * S, 10 * C, 10)
		glScalef(5, 5, 5)
		glCallList(graphics.lists.moon)

@WorldBound()
@Unanchorable()
class Zanyrod:
	def __init__(self, spot):
		self.init(spot = spot)
		self.tzany = 0
		self.think(0)
		self.h = -30

	def think(self, dt):
		self.tzany += dt
		C, S = math.CS(0.7 * self.tzany)
		axis = world.linsum(self.left, C, self.forward, S)
		up = world.rot(axis, self.up, 4 * self.tzany)
		state.rmoon = up

	def drawmoon(self):
		pass


@WorldBound()
class Sequencer:
	def __init__(self, spot):
		self.init(spot = spot)
		self.t = 0
		self.alive = True
		self.seq = ["Zodiac"]

	def think(self, dt):
		self.t += dt

	def draw(self):
		if math.cycle(15 * self.t) + self.t < 2:
			return
		if abs(math.cycle(0.1 * self.t) - 0.1) < 0.04 and 20 * self.t % 1 > 0.5:
			return
		glRotatef(40 * self.t % 360, 0, 0, 1)
		glTranslatef(0, 0, math.mix(math.cycle(0.5 * self.t), 13, 14))
		glScale(0.3, 0.3, 0.3)
		if abs(math.cycle(0.2 * self.t) - 0.7) < 0.02 and 20 * self.t % 1 > 0.5:
			v = [0.5, 1, 2]
			random.shuffle(v)
			glScale(*v)
		state.getisland(self.seq[int(self.t * 0.5) % len(self.seq)]).draw()

	def adraw(self):
		glCallList(graphics.lists.discs["white"][3])
		


@WorldBound()
class Disc:
	def __init__(self, spot, color):
		self.init(spot = spot)
		self.color = color
		self.t = 0
		self.h = -4.8
		self.alive = True
		self.fading = False
		self.ffade = 0

	def think(self, dt):
		self.t += dt
		self.ffade = math.approach(self.ffade, 0 if self.fading else 1, dt / 4)
		if self.ffade == 0 and self.fading:
			self.alive = False

	def draw(self):
		glTranslatef(0, 0, -10 * (1 - self.ffade))
		dh = state.tideat(self.up) - self.h
		if dh > 0:
			dx = 0.5 * dh * graphics.noiseat([0.5, 0.5, self.t], [2, 1.2, 0.7], seed=self.color)
			dy = 0.5 * dh * graphics.noiseat([4.5, 4.5, self.t], [2, 1.2, 0.7], seed=self.color)
			da = 0.5 * dh * graphics.noiseat([0.5, 4.5, self.t], [2, 1.2, 0.7], seed=self.color)
			db = 0.5 * dh * graphics.noiseat([4.5, 0.5, self.t], [2, 1.2, 0.7], seed=self.color)
			theta = math.degrees(math.atan2(da, db))
			s = 1 + 0.02 * math.length([da, db])
			glRotatef(theta, 0, 0, 1)
			glScale(s, 1/s, 1)
			glRotatef(-theta, 0, 0, 1)
			glTranslatef(dx, dy, 0)
		alpha = self.ffade
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
		if math.cycle(self.ffade * 40) + 10 * self.ffade > 7:
			glCallList(graphics.lists.discs[self.color][3])

	def touched(self, vmin = 1):
		if self.ffade < 1:
			return False
		d = world.R * math.distance(self.up, state.you.up)
		v = math.length(state.you.vecho)
		return d < 14 and v < vmin and state.tideat(self.up) < self.h + 1

	def fade(self):
		self.fading = True

	def unfade(self):
		self.t = 0
		self.alive = True
		self.fading = False

class Raisedisc(Disc):
	def __init__(self, spot, color = "black"):
		Disc.__init__(self, spot, color)
		self.tide0 = 2
		self.tide1 = 8
		self.raising = False
		self.h = 0
		self.away = True
	def think(self, dt):
		Disc.think(self, dt)
		(tide, aspeed) = (self.tide1, 1) if self.raising else (self.tide0, 0.2)
		state.tide = math.approach(state.tide, tide, aspeed * dt)
		if state.tide == self.tide1:
			self.raising = False
		if not self.fading:
			state.dmoon = 1 / math.fadebetween(state.tide, self.tide0, 1 / 200, self.tide1, 1 / 20)
		d = world.R * math.distance(self.up, state.you.up)
		if d > 25:
			self.away = True
		if not self.raising and self.away and self.touched(vmin = 100):
			self.away = False
			self.raising = True
			sound.play("find1")
			sound.play("rumble")
	def draw(self):
		Disc.draw(self)
		if not self.fading:
			glTranslatef(0, 0, 5 + 0.3 * state.dmoon)
			glScalef(5, 5, 5)
			glCallList(graphics.lists.moon)

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
		self.tbloom = 0

@Lifetime(1)
@WorldBound()
class Splash:
	def __init__(self, spot, v, fsplash = None):
		self.init(spot = spot)
		self.ospot = world.randomspot()
		self.v = v
		self.fsplash = math.fadebetween(math.length(v), 0, 0.3, 60, 1) if fsplash is None else fsplash
		self.lifetime = 0.4 * self.fsplash
		self.h = 0
		self.move(0.02)
	def move(self, dt):
		self.spotrot(math.norm(world.cross(self.up, self.v)), math.length(self.v) * dt / world.R)
	def think(self, dt):
		from . import quest
		v = state.you.getfullv()
		self.v = math.mix(self.v, v, 1 - math.exp(-dt * 6))
		
		self.h = state.tideat(self.up) + 1 + 6 * self.fsplash * self.f * (1 - self.f)
		self.move(dt)
		if not self.alive:
			quest.pourwater(self.up)
	def draw(self):
		glScale(1, 1, 0.2)
		f, l, u = self.ospot
		glMultMatrixf([*f,0,  *l,0,  *u,0,  0,0,0,1])
		s = math.mix(0.3, 1, self.fsplash) * math.mix(0.3, 1, self.f ** 0.4) * 14
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
		self.t = 0
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
		self.t += dt
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
		glRotatef(100 * self.t % 360, 0, 0, 1)
		glTranslatef(0, 0, math.cycle(0.1 * self.t))
		glCallList(graphics.lists.seed)


def init():
	state.you = You(world.oct0)
	state.moonrod = None
	if False:
#		state.moonrod = Moonrod(spot = world.oct0)
		state.moonrod = Zanyrod(spot = world.oct0)
		state.moonrod.h = 5
		state.tide = 16

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
#			(0.10, 3, j * math.phi % 1),
#			(0.07, 5, j * math.phi ** 2 % 1),
			(0.05, 7, j * math.phi ** 3 % 1),
			(0.03, 17, j * math.phi ** 4 % 1),
			(0.02, 29, j * math.phi ** 5 % 1),
		]
		for j in range(10, 16)
	]
	Rs = [math.mix(25, 35, j * math.phi % 1) for j in range(6)]
	for name, ispot, ispec, R in zip(names, ispots, ispecs, Rs):
		if name == "Apex":
			ispec.append((0.25, 3, 0.1))
		if name == "Botany":
			ispec.append((0.25, 5, 0.1))
		if name == "Cruz":
			ispec.append((0.25, 2, 0.1))
		if name == "Xenia":
			ispec.append((0.25, 4, 0.1))
		if name == "Yastreb":
			ispec.append((0.20, 3, 0.4))
			ispec.append((0.20, 7, 0.4))
		graphics.renderisland(name, ispec, R)
		state.islands.append(Island(name, ispot, ispec, R))

#	state.getisland("Zodiac").ktree = 1

