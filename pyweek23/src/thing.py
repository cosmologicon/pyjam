from __future__ import division
import pygame, math, random
from . import view, ptext, state, util, image, settings
from . import scene, visitscene
from .enco import Component
from .util import F

# Positive x is right
# Positive y is down

# positive rotational motion is clockwise
# angle of 0 is right
# angle of tau/4 is down

def getattribs(obj, kw, *anames):
	for aname in anames:
		if aname in kw:
			setattr(obj, aname, kw[aname])

class WorldBound(Component):
	def setstate(self, **kw):
		getattribs(self, kw, "x", "y")

class Lives(Component):
	def __init__(self):
		self.alive = True
		self.t = 0
	def setstate(self, **kw):
		getattribs(self, kw, "t", "alive")
	def think(self, dt):
		self.t += dt
	def die(self):
		self.alive = False

class Lifetime(Component):
	def __init__(self, lifetime = 1):
		self.lifetime = lifetime
		self.f = 0
	def setstate(self, **kw):
		getattribs(self, kw, "lifetime", "f")
	def think(self, dt):
		self.f = 1 if self.lifetime <= 0 else util.clamp(self.t / self.lifetime, 0, 1)
		if self.f >= 1:
			self.die()

class LinearMotion(Component):
	def __init__(self):
		self.vx = 0
		self.vy = 0
	def setstate(self, **kw):
		getattribs(self, kw, "vx", "vy")
	def think(self, dt):
		self.x += dt * self.vx
		self.y += dt * self.vy

class Knockable(Component):
	def __init__(self):
		self.kx = 0
		self.ky = 0
	def setstate(self, **kw):
		getattribs(self, kw, "kx", "ky")
	def knock(self, dkx, dky):
		self.kx = dkx
		self.ky = dky
	def think(self, dt):
		if not self.kx and not self.ky: return
		k = math.sqrt(self.kx ** 2 + self.ky ** 2)
		d = 300 * dt
		if k < d:
			dx, dy = self.kx, self.ky
			self.kx, self.ky = 0, 0
		else:
			dx, dy = util.norm(self.kx, self.ky, d)
			self.kx -= dx
			self.ky -= dy
		self.x += dx
		self.y += dy

class MovesWithArrows(Component):
	def __init__(self, **kw):
		self.vx = 0
		self.vy = 0
	def move(self, dt, dx, dy):
		if dx: self.vx = state.speed * dx
		if dy: self.vy = state.speed * dy
		self.x += state.speed * dx * dt
		self.y += state.speed * dy * dt
	def think(self, dt):
		f = math.exp(-10 * dt)
		self.vx *= f
		self.vy *= f

class SeeksEnemies(Component):
	def __init__(self, v0):
		self.v0 = v0
	def setstate(self, **kw):
		getattribs(self, kw, "v0")
	def think(self, dt):
		target, r = None, 200
		for e in state.enemies:
			d = math.sqrt((self.x - e.x) ** 2 + (self.y - e.y) ** 2)
			if d < r:
				target, r = e, d
		if target:
			ax, ay = util.norm(target.x - self.x, target.y - self.y, 2000)
		else:
			ax, ay = 2000, 0
		self.vx, self.vy = util.norm(self.vx + dt * ax, self.vy + dt * ay, self.v0)

class SeeksFormation(Component):
	def __init__(self, vmax, accel):
		self.vmax = vmax
		self.v = 0
		self.vx = 0
		self.vy = 0
		self.accel = accel
		self.target = None
	def setstate(self, **kw):
		getattribs(self, kw, "vmax", "v", "vx", "vy", "accel", "steps", "target")
		self.steps = list(self.steps)
	def think(self, dt):
		while self.steps and self.steps[0][0] < self.t:
			self.target = self.steps[0][1:3]
			self.steps = self.steps[1:]
		if not self.target:
			return
		self.v = min(self.v + dt * self.accel, self.vmax)
		tx, ty = self.target
		dx, dy = tx - self.x, ty - self.y
		d = math.sqrt(dx * dx + dy * dy)
		if d < 0.01:
			v = 100
		else:
			v = min(self.v, math.sqrt(2 * 2 * self.accel * d) + 1)
		if v * dt >= d:
			self.x, self.y = self.target
			self.target = None
			self.v = 0
			self.vx = 0
			self.vy = 0
		else:
			self.vx = v * dx / d
			self.vy = v * dy / d
			self.x += self.vx * dt
			self.y += self.vy * dt

class Cycloid(Component):
	def setstate(self, **kw):
		getattribs(self, kw, "x0", "y0", "dy0", "vy0", "cr", "dydtheta")
		self.think(0)
	def think(self, dt):
		dy = self.dy0 + self.vy0 * self.t
		yc = self.y0 + dy
		dycdt = self.vy0
		xc = self.x0
		theta = math.tau / 2 + dy / self.dydtheta
		dthetadt = self.vy0 / self.dydtheta
		S, C = math.sin(theta), math.cos(theta)
		self.x = xc + C * self.cr
		self.y = yc + S * self.cr
		self.vx = -S * dthetadt * self.cr
		self.vy = dycdt + C * dthetadt * self.cr


class SeeksHorizontalPosition(Component):
	def __init__(self, vxmax, accel):
		self.vxmax = vxmax
		self.vx = 0
		self.xaccel = accel
		self.xtarget = None
	def setstate(self, **kw):
		getattribs(self, kw, "vxmax", "vx", "xaccel", "xtarget")
	def think(self, dt):
		if self.xtarget is None: return
		self.vx = abs(self.vx)
		self.vx = min(self.vx + dt * self.xaccel, self.vxmax)
		dx = abs(self.xtarget - self.x)
		if dx < 0.01:
			v = 100
		else:
			v = min(self.vx, math.sqrt(2 * 2 * self.xaccel * dx) + 1)
		if v * dt >= dx:
			self.x = self.xtarget
			self.xtarget = None
			self.vx = 0
		else:
			self.vx = v if self.xtarget > self.x else -v
			self.x += self.vx * dt

class SeeksHorizontalSinusoid(Component):
	def __init__(self, vxmax0, xaccel0, xomega, xr):
		self.vxmax0 = vxmax0
		self.vx0 = 0
		self.x0 = None
		self.xaccel0 = xaccel0
		self.xomega = xomega
		self.xr = xr
		self.xtarget0 = None
		self.xtheta = 0
	def setstate(self, **kw):
		getattribs(self, kw, "vxmax0", "vx0", "x0", "xaccel0", "xomega", "xtheta" "xr", "xtarget0", "x", "vx")
	def think(self, dt):
		if self.x0 is None:
			self.x0 = self.x
		if self.xtarget0 is not None:
			self.vx0 = abs(self.vx0)
			self.vx0 = min(self.vx0 + dt * self.xaccel0, self.vxmax0)
			dx = abs(self.xtarget0 - self.x0)
			if dx < 0.01:
				v = 100
			else:
				v = min(self.vx0, math.sqrt(2 * 2 * self.xaccel0 * dx) + 1)
			if v * dt >= dx:
				self.x0 = self.xtarget0
				self.xtarget0 = None
				self.vx0 = 0
			else:
				self.vx0 = v if self.xtarget0 > self.x0 else -v
				self.x0 += self.vx0 * dt
		self.xtheta += self.xomega * dt
		self.x = self.x0 + self.xr * math.sin(self.xtheta)
		self.vx = self.vx0 + self.xr * self.xomega * math.cos(self.xtheta)

class VerticalSinusoid(Component):
	def __init__(self, yomega, yrange, y0 = 0):
		self.yomega = yomega
		self.yrange = yrange
		self.y0 = y0
		self.ytheta = 0
	def setstate(self, **kw):
		getattribs(self, kw, "yomega", "yrange", "y0", "ytheta")
	def think(self, dt):
		self.ytheta += dt * self.yomega
		self.y = self.y0 + self.yrange * math.sin(self.ytheta)
		self.vy = self.yrange * self.ytheta * math.cos(self.ytheta)


class FiresWithSpace(Component):
	def __init__(self):
		self.tshot = 0  # time since last shot
	def setstate(self, **kw):
		getattribs(self, kw, "tshot")
	def think(self, dt):
		self.tshot += dt
	def act(self):
		if self.tshot > state.reloadtime:
			self.shoot()
	def getcharge(self):
		t = self.tshot - state.reloadtime
		if t <= 0: return 0
		if t >= state.chargetime: return state.maxcharge
		return t / state.chargetime * state.maxcharge
	def getdamage(self):
		return state.basedamage + int(self.getcharge())
	def getbulletsize(self):
		return 3 * (state.basedamage + self.getcharge()) ** 0.3
	def shoot(self):
		r = self.r + 15
		x0, y0 = self.x + r, self.y
		bullet = GoodBullet(
			x = self.x + r, y = self.y,
			vx = 500, vy = 0,
			r = self.getbulletsize(),
			damage = self.getdamage()
		)
		state.goodbullets.append(bullet)
		for jvshot in range(state.vshots):
			dx, dy = -6 * (jvshot + 1), 8 * (jvshot + 1)
			state.goodbullets.append(RangeGoodBullet(
				x = x0 + dx, y = y0 + dy, vx = 500, vy = 0, r = 3, damage = 1, lifetime = 0.2))
			state.goodbullets.append(RangeGoodBullet(
				x = x0 + dx, y = y0 - dy, vx = 500, vy = 0, r = 3, damage = 1, lifetime = 0.2))
		self.tshot = 0
	def draw(self):
		charge = self.getcharge()
		if charge <= 0: return
		pos = view.screenpos((self.x + self.r * 7, self.y))
		r = F(view.Z * self.getbulletsize())
		color = (255, 255, 255) if self.t * 4 % 1 > 0.5 else (200, 200, 255)
		pygame.draw.circle(view.screen, color, pos, r)

class MissilesWithSpace(Component):
	def __init__(self):
		self.tmissile = 0  # time since last shot
		self.jmissile = 0
	def setstate(self, **kw):
		getattribs(self, kw, "tmissile", "jmissile")
	def think(self, dt):
		self.tmissile += dt
	def act(self):
		if self.tmissile > state.missiletime:
			self.shootmissile()
	def shootmissile(self):
		dx, dy = util.norm(*[[0, -3], [0, 3]][self.jmissile])
		r = self.r + 5
		missile = GoodMissile(
			x = self.x + r * dx, y = self.y + r * dy,
			vx = 1000 * dx, vy = 1000 * dy
		)
		state.goodbullets.append(missile)
		self.jmissile += 1
		self.jmissile %= 2
		self.tmissile = 0

class CShotsWithSpace(Component):
	def __init__(self):
		self.tcshot = 0  # time since last shot
	def setstate(self, **kw):
		getattribs(self, kw, "tcshot")
	def think(self, dt):
		self.tcshot += dt
	def act(self):
		if self.tcshot > state.cshottime:
			self.cshot()
	def cshot(self):
		r = self.r + 5
		for jshot in range(2, 11):
			theta = jshot / 12 * math.tau
			dx, dy = math.cos(theta), math.sin(theta)
			bullet = GoodBullet(
				x = self.x + r * dx, y = self.y + r * dy,
				vx = 500 * dx, vy = 500 * dy,
				r = 5,
				damage = 5
			)
			state.goodbullets.append(bullet)
			self.tcshot = 0

class YouBound(Component):
	def __init__(self, omega, R):
		self.omega = omega
		self.R = R
	def think(self, dt):
		theta = self.omega * self.t
		self.x = state.you.x + self.R * math.cos(theta)
		self.y = state.you.y + self.R * math.sin(theta)

class BossBound(Component):
	def __init__(self, diedelay = 0):
		self.diedelay = diedelay
		self.target = None
	def setstate(self, **kw):
		getattribs(self, kw, "target", "diedelay")
	def think(self, dt):
		if not self.alive:
			return
		if self.target and not self.target.alive:
			self.diedelay -= dt
			if self.diedelay <= 0:
				self.die()

class Tumbles(Component):
	def __init__(self, omega):
		self.omega = omega
		self.theta = 0
	def setstate(self, **kw):
		getattribs(self, kw, "theta", "omega")
	def think(self, dt):
		self.theta += self.omega * dt

class EncirclesBoss(Component):
	def __init__(self):
		self.vx = 0
		self.vy = 0
	def setstate(self, **kw):
		getattribs(self, kw, "omega", "R", "theta")
	def think(self, dt):
		if not self.alive or not self.target.alive:
			return
		self.theta += self.omega * dt
		S, C = math.sin(self.theta), math.cos(self.theta)
		self.x = self.target.x + self.R * C
		self.y = self.target.y + self.R * S
		self.vx = -S * self.R * self.omega
		self.vy = C * self.R * self.omega

class SinusoidsAcross(Component):
	def __init__(self, varc = 50, harc = 50, p0arc = 0):
		self.vx = 0
		self.vy = 0
		self.varc = varc
		self.harc = harc
		self.p0arc = p0arc
	def setstate(self, **kw):
		getattribs(self, kw, "x0arc", "y0arc", "dxarc", "dyarc", "varc", "harc", "p0arc")
	def think(self, dt):
		if not self.alive or not self.target.alive:
			return
		p = self.p0arc + self.varc * self.t
		dpdt = self.varc
		darc = math.sqrt(self.dxarc ** 2 + self.dyarc ** 2)
		beta = math.tau * p / darc
		dbetadt = math.tau * dpdt / darc
		h = self.harc * math.sin(beta)
		dhdt = self.harc * dbetadt * math.cos(beta)
		C, S = util.norm(self.dxarc, self.dyarc)
		self.x = self.x0arc + p * C - h * S
		self.y = self.y0arc + p * S + h * C
		self.vx = dpdt * C - dhdt * S
		self.vy = dpdt * S + dhdt * C

class SpawnsCobras(Component):
	def __init__(self, dtcobra = 2):
		self.tcobra = 0
		self.dtcobra = dtcobra
		self.jcobra = 0
	def setstate(self, **kw):
		getattribs(self, kw, "tcobra", "dtcobra", "jcobra")
	def think(self, dt):
		self.tcobra += dt
		while self.tcobra > self.dtcobra:
			self.spawncobra()
			self.tcobra -= self.dtcobra
	def spawncobra(self):
		top = self.jcobra % 2 == 1
		x0 = self.jcobra * math.phi % 1 * 500 - 100
		y0 = -state.yrange if top else state.yrange
		dx = -300
		dy = (300 if top else -300) * (1 + self.jcobra * math.phi % 1 * 0.4)
		h = 80
		p0 = -50
		for jseg, r in enumerate((40, 38, 36, 34, 32, 30, 28, 26, 24, 23, 22, 21, 20)):
			diedelay = 0.5 + 0.1 * jseg
			snake = Cobra(x0arc = x0, y0arc = y0, dxarc = dx, dyarc = dy, p0arc = p0, harc = h,
				r = r, target = self, diedelay = diedelay)
			state.enemies.append(snake)
			p0 -= r * 0.8
		self.jcobra += 1
	
class SpawnsSwallows(Component):
	def __init__(self, nswallow):
		self.nswallow = nswallow
		self.tfreak = 0
	def setstate(self, **kw):
		getattribs(self, kw, "nswallow")
		self.swallows = []
		for jswallow in range(self.nswallow):
			theta = jswallow * math.tau / self.nswallow
			swallow = Swallow(target = self, omega = 1, R = self.r, theta = theta)
			self.swallows.append(swallow)
			state.enemies.append(swallow)
	def think(self, dt):
		if self.tfreak:
			self.tfreak = max(self.tfreak - dt, 0)
			if self.tfreak == 0:
				self.xomega /= 3
				self.yomega /= 3
				if not self.swallows:
					self.die()
		elif any(not s.alive for s in self.swallows):
			self.tfreak = 1.5
			self.xomega *= 5
			self.yomega *= 5
			self.swallows = [s for s in self.swallows if s.alive]
			for s in self.swallows:
				s.omega *= 1.4

	
class SpawnsHerons(Component):
	def __init__(self, dtheron):
		self.dtheron = dtheron
		self.theron = 0
		self.jheron = 0
	def setstate(self, **kw):
		getattribs(self, kw, "theron", "dtheron", "jheron")
	def think(self, dt):
		self.theron += dt
		while self.theron >= self.dtheron:
			heron = Heron(x = 600, y = self.y, vx = -60, vy = 0, target = self)
			state.enemies.append(heron)
			self.jheron += 1
			self.theron -= self.dtheron

class Collides(Component):
	def __init__(self, r):
		self.r = r
	def setstate(self, **kw):
		getattribs(self, kw, "r")

class ConstrainToScreen(Component):
	def __init__(self, xmargin = 0, ymargin = 0):
		self.xmargin = xmargin
		self.ymargin = ymargin
	def think(self, dt):
		dxmax = 427 / view.Z - self.r - self.xmargin
		self.x = util.clamp(self.x, view.x0 - dxmax, view.x0 + dxmax)
		dymax = state.yrange - self.r - self.ymargin
		self.y = util.clamp(self.y, -dymax, dymax)

class DisappearsOffscreen(Component):
	def __init__(self, offscreenmargin = 20):
		self.offscreenmargin = offscreenmargin
	def setstate(self, **kw):
		getattribs(self, kw, "offscreenmargin")
	def think(self, dt):
		x = self.x - view.x0
		xmax = 427 / view.Z + self.r + self.offscreenmargin
		ymax = state.yrange + self.r + self.offscreenmargin
		if x * self.vx > 0 and abs(x) > xmax:
			self.die()
		if self.y * self.vy > 0 and abs(self.y) > ymax:
			self.die()

class RoundhouseBullets(Component):
	def __init__(self):
		self.tbullet = 0
		self.dtbullet = 0.3
		self.nbullet = 20
		self.vbullet = 50
		self.jbullet = 0
	def think(self, dt):
		self.tbullet += dt
		while self.tbullet >= self.dtbullet:
			for jtheta in range(3):
				theta = (self.jbullet / self.nbullet + jtheta / 3) * math.tau
				dx, dy = math.cos(theta), math.sin(theta)
				r = self.r + 2
				bullet = BadBullet(
					x = self.x + r * dx,
					y = self.y + r * dy,
					vx = self.vbullet * dx,
					vy = self.vbullet * dy
				)
				state.badbullets.append(bullet)
			self.tbullet -= self.dtbullet
			self.jbullet += 1

class ABBullets(Component):
	def __init__(self, nbullet, dtbullet):
		self.tbullet = 0
		self.nbullet = nbullet
		self.dtbullet = dtbullet
		self.vbullet = 50
		self.jbullet = 0
	def think(self, dt):
		self.tbullet += dt
		while self.tbullet >= self.dtbullet:
			for jtheta in range(self.nbullet):
				theta = (jtheta + self.jbullet * 0.5) / self.nbullet * math.tau
				dx, dy = math.cos(theta), math.sin(theta)
				r = self.r + 2
				bullet = BadBullet(
					x = self.x + r * dx,
					y = self.y + r * dy,
					vx = self.vbullet * dx,
					vy = self.vbullet * dy
				)
				state.badbullets.append(bullet)
			self.tbullet -= self.dtbullet
			self.jbullet += 1
			self.jbullet %= 2

class Visitable(Component):
	def setstate(self, **kw):
		getattribs(self, kw, "name")
	def visit(self):
		if self.name in state.visited:
			return
		state.visited.add(self.name)
		scene.push(visitscene, self.name)
	def draw(self):
		if self.name in state.visited:
			return
		if self.t % 2 > 1.5:
			return
		pos = view.screenpos((self.x + self.r, self.y - self.r))
		ptext.draw("HELP!", center = pos, fontsize = F(30))

class DiesOnCollision(Component):
	def hit(self, target = None):
		self.die()

class HurtsOnCollision(Component):
	def __init__(self, damage = 1):
		self.damage = damage
	def setstate(self, **kw):
		getattribs(self, kw, "damage")
	def hit(self, target = None):
		if target is not None:
			target.hurt(self.damage)

class KnocksOnCollision(Component):
	def __init__(self, dknock = 10):
		self.dknock = dknock
	def setstate(self, **kw):
		getattribs(self, kw, "dknock")
	def hit(self, target = None):
		if target is not None:
			target.knock(*util.norm(target.x - self.x, target.y - self.y, self.dknock))

class HasHealth(Component):
	def __init__(self, hp0):
		self.hp0 = self.hp = hp0
	def setstate(self, **kw):
		getattribs(self, kw, "hp")
	def hurt(self, damage):
		if self.hp <= 0: return
		self.hp -= damage
		if self.hp <= 0: self.die()

class InfiniteHealth(Component):
	def hurt(self, damage):
		pass

class Collectable(Component):
	def think(self, dt):
		dx, dy = state.you.x - self.x, state.you.y - self.y
		d = math.sqrt(dx * dx + dy * dy)
		if d < state.rmagnet:
			dx, dy = util.norm(dx, dy, 300 * dt)
			self.x += dx
			self.y += dy
	def collect(self):
		self.die()

class HealsOnCollect(Component):
	def __init__(self, heal = 1):
		self.heal = heal
	def setstate(self, **kw):
		getattribs(self, kw, "heal")
	def collect(self):
		state.heal(self.heal)

class MissilesOnCollect(Component):
	def __init__(self, nmissile = 40):
		self.nmissile = nmissile
	def setstate(self, **kw):
		getattribs(self, kw, "nmissile")
	def collect(self):
		r = self.r + 5
		for jmissile in range(self.nmissile):
			theta = math.tau * (jmissile + 0.5) * math.phi
			dx, dy = math.cos(theta), math.sin(theta)
			missile = GoodMissile(
				x = self.x + r * dx, y = self.y + r * dy,
				vx = 1000 * dx, vy = 1000 * dy
			)
			t = jmissile / self.nmissile * 0.2
			state.spawners.append(Spawner(egg = missile, collection = state.goodbullets, lifetime = t))

class SlowsOnCollect(Component):
	def __init__(self, tslow = 5):
		self.tslow = tslow
	def setstate(self, **kw):
		getattribs(self, kw, "tslow")
	def collect(self):
		state.tslow = max(state.tslow, self.tslow)

class Spawns(Component):
	def setstate(self, **kw):
		getattribs(self, kw, "egg", "collection")
	def die(self):
		self.collection.append(self.egg)

class DrawImage(Component):
	def __init__(self, imgname, imgscale = 1):
		self.imgname = imgname
		self.imgscale = imgscale
	def setstate(self, **kw):
		getattribs(self, kw, "imgname", "imgscale")
	def draw(self):
		scale = 0.01 * self.r * self.imgscale
		image.Gdraw(self.imgname, pos = (self.x, self.y), scale = scale)
		if settings.DEBUG:
			pos = view.screenpos((self.x, self.y))
			r = F(view.Z * self.r)
			pygame.draw.circle(view.screen, (255, 0, 0), pos, r, F(1))

class DrawFacingImage(Component):
	def __init__(self, imgname, imgscale = 1, ispeed = 0):
		self.imgname = imgname
		self.imgscale = imgscale
		self.ispeed = ispeed
	def setstate(self, **kw):
		getattribs(self, kw, "imgname", "imgscale")
	def draw(self):
		scale = 0.01 * self.r * self.imgscale
		y = -self.vy
		x = self.vx + self.ispeed
		angle = 0 if x == 0 and y == 0 else math.degrees(math.atan2(y, x))
		if settings.portrait:
			angle += 90
		image.Gdraw(self.imgname, pos = (self.x, self.y), scale = scale, angle = angle)
		if settings.DEBUG:
			pos = view.screenpos((self.x, self.y))
			r = F(view.Z * self.r)
			pygame.draw.circle(view.screen, (255, 0, 0), pos, r, F(1))

class DrawAngleImage(Component):
	def __init__(self, imgname, imgscale = 1):
		self.imgname = imgname
		self.imgscale = imgscale
	def setstate(self, **kw):
		getattribs(self, kw, "imgname", "imgscale")
	def draw(self):
		scale = 0.01 * self.r * self.imgscale
		angle = math.degrees(-self.theta)
		if settings.portrait:
			angle += 90
		image.Gdraw(self.imgname, pos = (self.x, self.y), scale = scale, angle = angle)
		if settings.DEBUG:
			pos = view.screenpos((self.x, self.y))
			r = F(view.Z * self.r)
			pygame.draw.circle(view.screen, (255, 0, 0), pos, r, F(1))

class DrawBox(Component):
	def __init__(self, boxname, boxcolor = (120, 120, 120)):
		self.boxname = boxname
		self.boxcolor = boxcolor
	def draw(self):
		pos = view.screenpos((self.x, self.y))
		r = F(view.Z * self.r)
		pygame.draw.circle(view.screen, self.boxcolor, pos, r)
		ptext.draw(self.boxname, center = pos, color = "white", fontsize = F(14))

class FlashesOnInvulnerable(Component):
	def draw(self):
		self.boxcolor = (100, 0, 0) if state.tinvulnerable * 6 % 1 > 0.5 else (100, 100, 100)


class DrawFlash(Component):
	def __init__(self):
		self.dtflash = random.random()
	def draw(self):
		pos = view.screenpos((self.x, self.y))
		r = F(view.Z * self.r)
		color = (255, 120, 120) if (self.t + self.dtflash) * 5 % 1 > 0.5 else (255, 255, 0)
		pygame.draw.circle(view.screen, color, pos, r)

class DrawGlow(Component):
	def __init__(self):
		self.dtflash = random.random()
	def draw(self):
		pos = view.screenpos((self.x, self.y))
#		pygame.draw.circle(view.screen, (200, 200, 255), pos, F(view.Z * self.r * 2))
		pygame.draw.circle(view.screen, (200, 200, 255), pos, F(view.Z * self.r * 1))

@WorldBound()
@Lives()
@MovesWithArrows()
@Knockable()
@FiresWithSpace()
@MissilesWithSpace()
@CShotsWithSpace()
@Collides(5)
@ConstrainToScreen(5, 5)
@FlashesOnInvulnerable()
@DrawFacingImage("you", 5, 1000)
class You(object):
	def __init__(self, **kw):
		self.setstate(**kw)
	def hurt(self, damage):
		state.takedamage(damage)

@WorldBound()
@YouBound(5, 25)
@Lives()
@Collides(4)
@InfiniteHealth()
@DrawBox("zap")
class Companion(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@WorldBound()
@Lives()
@Collides(60)
@LinearMotion()
@InfiniteHealth()
@DrawBox("planet")
@Visitable()
class Planet(object):
	def __init__(self, **kw):
		self.setstate(vx = -state.scrollspeed, vy = 0, **kw)

@WorldBound()
@Lives()
@Collides(16)
@LinearMotion()
@InfiniteHealth()
@Tumbles(1)
@DrawAngleImage("capsule", 1.7)
@Visitable()
class Capsule(object):
	def __init__(self, **kw):
		self.setstate(vx = -state.scrollspeed, vy = 0, **kw)

@WorldBound()
@Lives()
@Collides(3)
@LinearMotion()
@DiesOnCollision()
@HurtsOnCollision()
@DisappearsOffscreen()
@DrawFlash()
class BadBullet(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@WorldBound()
@Lives()
@Collides(3)
@LinearMotion()
@DiesOnCollision()
@HurtsOnCollision()
@DisappearsOffscreen()
@DrawGlow()
class GoodBullet(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@WorldBound()
@Lives()
@Lifetime(0.5)
@Collides(3)
@LinearMotion()
@DiesOnCollision()
@HurtsOnCollision()
@DisappearsOffscreen()
@DrawGlow()
class RangeGoodBullet(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@WorldBound()
@Lives()
@Collides(3)
@SeeksEnemies(300)
@LinearMotion()
@DiesOnCollision()
@HurtsOnCollision()
@DisappearsOffscreen()
@DrawGlow()
class GoodMissile(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@WorldBound()
@Lives()
@HasHealth(20)
@Collides(60)
@RoundhouseBullets()
@SeeksHorizontalPosition(30, 30)
@VerticalSinusoid(0.4, 120)
@HurtsOnCollision(3)
@KnocksOnCollision(40)
@SpawnsCobras()
@DrawBox("medusa")
class Medusa(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@WorldBound()
@Lives()
@InfiniteHealth()
@Collides(80)
#@RoundhouseBullets()
@SeeksHorizontalSinusoid(30, 30, 0.8, 100)
@VerticalSinusoid(0.6, 120)
@HurtsOnCollision(3)
@KnocksOnCollision(40)
@SpawnsSwallows(6)
@SpawnsHerons(3)
@DrawImage("egret", 1.4)
class Egret(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@WorldBound()
@BossBound()
@EncirclesBoss()
@Lives()
@HasHealth(20)
@Collides(30)
@HurtsOnCollision(3)
@KnocksOnCollision(40)
@DrawAngleImage("swallow", 1.3)
class Swallow(object):
	def __init__(self, **kw):
		self.setstate(**kw)
		self.think(0)


@WorldBound()
@BossBound()
@EncirclesBoss()
@Lives()
@InfiniteHealth()
@Collides(4)
@HurtsOnCollision(3)
@KnocksOnCollision(40)
@DrawFacingImage("snake", 1.2, 0)
class Asp(object):
	def __init__(self, **kw):
		self.setstate(**kw)
		self.think(0)

@WorldBound()
@BossBound()
@SinusoidsAcross()
@Lives()
@InfiniteHealth()
@Collides(4)
@HurtsOnCollision(3)
@KnocksOnCollision(40)
@DrawFacingImage("snake", 1.2, 0)
class Cobra(object):
	def __init__(self, **kw):
		self.setstate(**kw)
		self.think(0)

@WorldBound()
@Lives()
@HasHealth(3)
@Collides(20)
@SeeksFormation(400, 400)
@DisappearsOffscreen()
@HurtsOnCollision(3)
@KnocksOnCollision(40)
@DrawFacingImage("duck", 1.2, -100)
class Duck(object):
	def __init__(self, **kw):
		self.setstate(**kw)


@WorldBound()
@Lives()
@HasHealth(2)
@Collides(20)
@Cycloid()
@DisappearsOffscreen(500)
@HurtsOnCollision(3)
@KnocksOnCollision(40)
@DrawBox("lark")
class Lark(object):
	def __init__(self, **kw):
		self.setstate(**kw)


@WorldBound()
@Lives()
@BossBound()
@HasHealth(10)
@Collides(20)
@LinearMotion()
@DisappearsOffscreen()
@HurtsOnCollision(3)
@KnocksOnCollision(40)
@ABBullets(12, 3)
@DrawBox("heron")
class Heron(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@WorldBound()
@Lives()
@LinearMotion()
@HasHealth(3)
@Collides(20)
@DisappearsOffscreen()
@HurtsOnCollision(3)
@KnocksOnCollision(40)
@DrawImage("rock-0", 0.39)
class Rock(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@WorldBound()
@Lives()
@Collides(5)
@LinearMotion()
@DrawBox("health")
@Collectable()
@HealsOnCollect()
class HealthPickup(object):
	def __init__(self, **kw):
		self.setstate(vx = -state.scrollspeed, vy = 0, **kw)

@WorldBound()
@Lives()
@Collides(5)
@LinearMotion()
@DrawBox("missiles")
@Collectable()
@MissilesOnCollect()
class MissilesPickup(object):
	def __init__(self, **kw):
		self.setstate(vx = -state.scrollspeed, vy = 0, **kw)

@WorldBound()
@Lives()
@Collides(5)
@LinearMotion()
@DrawBox("slow")
@Collectable()
@SlowsOnCollect()
class SlowPickup(object):
	def __init__(self, **kw):
		self.setstate(vx = -state.scrollspeed, vy = 0, **kw)

@Lives()
@Lifetime()
@Spawns()
class Spawner(object):
	def __init__(self, **kw):
		self.setstate(**kw)
	

