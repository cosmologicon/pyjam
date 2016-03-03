from __future__ import division
import math, random, pygame
from . import window, ptext, state, image, settings, background, control, sound, util
from .enco import Component
from .util import F

class WorldBound(Component):
	def __init__(self):
		self.x, self.y, self.z = 0, 0, 0
	def init(self, obj):
		if "pos" in obj:
			self.x, self.y, self.z = obj["pos"]
	def pos(self):
		return self.x, self.y, self.z
	def screenpos(self, dz = 0):
		return window.worldtoscreen(self.x, self.y, self.z + dz)

class Lifetime(Component):
	def __init__(self, lifetime = 1):
		self.lifetime = lifetime
		self.f = 0
	def think(self, dt):
		self.f = min(self.t / self.lifetime, 1)
		if self.f == 1:
			self.die()

class DrawName(Component):
	def __init__(self, hoverdz = 0):
		self.hoverdz = hoverdz
	def draw(self):
		pos = self.screenpos(dz = self.hoverdz * math.sin(2 * self.t))
		ptext.draw(self.__class__.__name__, center = pos, color = "red", fontsize = F(24), owidth = 1)

class DrawShip(Component):
	def __init__(self, imgname):
		self.imgname = imgname
	def init(self, obj):
		self.hphi0 = random.uniform(0, 100)
		self.homega = random.uniform(1.6, 2.3)
	def draw(self):
		pos = self.screenpos(dz = 0.5 * math.sin(self.homega * self.t + self.hphi0))
		frame = int(round(self.angle / 10)) % 36 * 10
		if control.isselected(self):
			imgname = "data/ships/%s-%04d-outline.png" % (self.imgname, frame)
			image.draw(imgname, pos, scale = 3)
		imgname = "data/ships/%s-%04d.png" % (self.imgname, frame)
		image.draw(imgname, pos, scale = 3)
	def drawshadow(self):
		pos = window.worldtoscreen(self.x, self.y, 0)
		image.draw("data/shadow.png", pos, scale = 1.6)

class FacesForward(Component):
	def __init__(self):
		self.angle = 0
		self.targetangle = 0
		self.omega = 500
	def init(self, obj):
		self.angle = self.targetangle = random.uniform(0, 360)
	def think(self, dt):
		if self.vx or self.vy:
			self.targetangle = math.degrees(math.atan2(self.vx, self.vy)) % 360
		dangle = (self.targetangle - self.angle + 180) % 360 - 180
		if dangle:
			f = abs(dangle / (self.omega * dt))
			if f >= 1:
				self.angle += dangle / f
			else:
				self.angle = self.targetangle

# A pad is a circular region around a building. Ships entering the pad can interact with the building.
class HasPad(Component):
	def __init__(self, rpad):
		self.rpad = rpad
	def init(self, obj):
		self.visitors = []
	def isnear(self, ship):	
		return (self.x - ship.x) ** 2 + (self.y - ship.y) ** 2 <= self.rpad ** 2
	def think(self, dt):
		visitors = list(filter(self.isnear, state.state.team))
		for ship in visitors:
			if ship not in self.visitors:
				self.onenter(ship)
		for ship in self.visitors:
			if ship not in visitors:
				self.onexit(ship)
		self.visitors = visitors
	def onenter(self, ship):
		pass
	def onexit(self, ship):
		pass

# Effects that bridge a building and a ship
class SeverableConnection(Component):
	def init(self, obj):
		self.building = obj["building"]
		self.ship = obj["ship"]
	def think(self, dt):
		self.x = (self.building.x + self.ship.x) / 2
		self.y = (self.building.y + self.ship.y) / 2
		self.z = (self.building.z + self.ship.z) / 2
		if not self.building.isnear(self.ship):
			self.die()

class Rechargeable(Component):
	def __init__(self, needmax):
		self.needmax = needmax
	def init(self, obj):
		# self.needs[None] is an unfulfillable need.
		self.needs = { k: 0 for k in self.needmax }
		for k, v in obj.items():
			if k == "need":
				self.needs[None] = v
			if k == "need0":
				self.needs[0] = v
			if k == "need1":
				self.needs[1] = v
			if k == "need2":
				self.needs[2] = v
	def addneed(self, needtype, amount):
		self.needs[needtype] = min(self.needs.get(needtype, 0) + amount, self.needmax[needtype])
	def charge(self, dt, chargerates):
		for k, v in chargerates.items():
			if k in self.needs and self.needs[k] > 0:
				self.needs[k] = max(self.needs[k] - dt * v, 0)
				if self.needs[k] == 0:
					self.oncharge(k)
	def think(self, dt):
		for ship in self.visitors:
			self.charge(dt, ship.chargerates)
	def draw(self):
		for k, v in self.needs.items():
			if k is None or not v:
				continue
			pos = self.screenpos(dz = -1)
			text = "need%s: %d/%d" % (k, int(self.needmax[k] - v), self.needmax[k])
			ptext.draw(text, center = pos, color = settings.ncolors[k], fontsize = F(24), owidth = 1)
	def oncharge(self, needtype):
		pass
	def onenter(self, ship):
		for k, v in ship.chargerates.items():
			if k in self.needs and self.needs[k] > 0:
				state.state.effects.append(ChargeEffect(building = self, ship = ship, chargetype = k))

class Discharges(Component):
	def __init__(self, dischargerate = 1):
		self.dischargerate = dischargerate
	def think(self, dt):
		for k, v in self.needs.items():
			if v and not any(k in ship.chargerates for ship in self.visitors):
				self.needs[k] = min(self.needs[k] + dt * self.dischargerate, self.needmax[k])

class RevealsOnCharge(Component):
	def __init__(self, rreveal = 20):
		self.rreveal = rreveal
	def oncharge(self, needtype):		
		background.reveal(self.x, self.y, self.rreveal)

class Charges(Component):
	def __init__(self, chargerates):
		self.chargerates = chargerates

class SeversOnCharge(Component):
	def think(self, dt):
		if not any(k in self.building.needs and self.building.needs[k] > 0 for k in self.ship.chargerates):
			self.die()

# Keeps track of how much of the team is nearby
class TracksProximity(Component):
	def draw(self):
		text = "nprox: %d" % len(self.visitors)
		pos = self.screenpos(dz = -1)
		ptext.draw(text, center = pos, color = "yellow", fontsize = F(24), owidth = 1)
	def onenter(self, ship):
		self.chime(len(self.visitors) + 1)
	def onexit(self, ship):
		self.chime(len(self.visitors) - 1)
	def chime(self, nprox):
		sound.play("proxchime-%d" % nprox)

class ApproachesTarget(Component):
	def __init__(self, speed = 2):
		self.target = None
		self.speed = speed
		self.vx = 0
		self.vy = 0
	def settarget(self, target):
		self.target = target
	def think(self, dt):
		if not self.target:
			return
		dx = self.target[0] - self.x
		dy = self.target[1] - self.y
		if not dx and not dy:
			self.target = None
			return
		d = self.speed * dt
		f = d / math.sqrt(dx ** 2 + dy ** 2)
		self.vx = f * dx / dt
		self.vy = f * dy / dt
		if f >= 1:
			self.x, self.y = self.target
			self.target = None
		else:
			self.x += f * dx
			self.y += f * dy

class BuildTarget(Component):
	def __init__(self):
		self.btarget = None
	def setbuildtarget(self, btarget):
		self.target = btarget.x, btarget.y
		self.btarget = btarget
	def think(self, dt):
		if self.btarget and not self.target:
			state.state.buildings.append(self.btarget)
			self.btarget = None

class DrawEllipses(Component):
	def __init__(self, r = 1, color = (255, 0, 255), width = 1):
		self.rellipse = r
		self.color = color
		self.width = width
	def draw(self):
		for dr in (0, 0.2, 0.4):
			r = (self.f * 1.4 - dr)
			if r > 1:
				continue
			r *= self.rellipse * window.Z
			w, h = F(r, r * window.fy)
			thick = F(self.width)
			if h <= 2 * thick:
				continue
			rect = pygame.Rect((0, 0, w, h))
			rect.center = self.screenpos()
			pygame.draw.ellipse(window.screen, self.color, rect, thick)

class NeedColored(Component):
	def init(self, obj):
		self.color = settings.ncolors[obj["needtype"]]

class DrawChargeEffect(Component):
	def init(self, obj):
		self.chargetype = obj["chargetype"]
	def draw(self):
		p0 = self.ship.screenpos()
		p1 = self.building.screenpos()
		color = settings.ncolors[self.chargetype]
		pygame.draw.line(window.screen, color, p0, p1, F(1))

class DrawBallLightning(Component):
	def init(self, obj):
		self.arcs = []
	def think(self, dt):
		self.arcs = [arc for arc in self.arcs if 0.06 * random.random() > dt]
		colors = [(255, 255, 0), (200, 200, 200), (255, 127, 127)]
		while len(self.arcs) < 200:
			color = random.choice(colors)
			dr = random.uniform(200, 500)
			self.arcs.append([color, self.t, dr, random.uniform(0, 1000), 0, 0])
		for arc in self.arcs:
			arc[3] += random.uniform(-20, 20) * dt
	def draw(self):
		for arc in self.arcs:
			color, t0, dr, theta, dx0, dy0 = arc
			r = dr * (self.t - t0)
			dx1 = F(r * math.sin(theta))
			dy1 = F(r * math.cos(theta))
			arc[4:6] = dx1, dy1
			x, y = self.screenpos()
			pygame.draw.line(window.screen, color, (x + dx0, y + dy0), (x + dx1, y + dy1), F(1))

class DrawShakyConnection(Component):
	def __init__(self, thick = 1):
		self.thick = thick
	def init(self, obj):
		self.pos0 = obj["pos0"]
		self.pos1 = obj["pos1"]
	def draw(self):
		dx0, dy0, dz0, dx1, dy1, dz1 = [random.gauss(0, 0.6) for _ in range(6)]
		x0, y0, z0 = self.pos0
		x1, y1, z1 = self.pos1
		p0 = window.worldtoscreen(x0 + dx0, y0 + dy0, z0 + dz0)
		p1 = window.worldtoscreen(x1 + dx1, y1 + dy1, z1 + dz1)
		pygame.draw.line(window.screen, self.color, p0, p1, F(self.thick))

class DrawSmoke(Component):
	def init(self, obj):
		self.plumes = []		
	def think(self, dt):
		self.plumes = [p for p in self.plumes if self.t - p[0] < p[1]]
		while len(self.plumes) < 20:
			angle = random.choice(list(range(10)))
			size = random.choice([2, 3, 4])
			dx = random.uniform(-30, 30)
			dy = random.uniform(-30, -80)
			t = random.uniform(2, 6)
			self.plumes.append((self.t, t, angle, size, dx, dy))
	def draw(self):
		for plume in self.plumes:
			t0, t, angle, s, dx, dy = plume
			dt = self.t - t0
			f = dt / t
			alpha = 1 * min(1 - f, 4 * f)
			x, y = self.screenpos()
			pos = x + F(dt * dx), y + F(dt * dy)
			image.draw("data/smoke.png", pos, scale = s, alpha = alpha)


@WorldBound()
class Thing(object):
	def __init__(self, **kwargs):
		self.init(kwargs)
		self.t = 0
		self.alive = True
	def draw(self):
		pass
	def think(self, dt):
		self.t += dt
	def die(self):
		self.alive = False

@ApproachesTarget(speed = 4)
@BuildTarget()
@FacesForward()
@DrawShip("tori")
@Charges({0: 1})
class ShipA(Thing):
	letter = "A"

@ApproachesTarget(speed = 8)
@BuildTarget()
@FacesForward()
@DrawShip("tori")
@Charges({1: 1})
class ShipB(Thing):
	letter = "B"

@ApproachesTarget(speed = 6)
@BuildTarget()
@FacesForward()
@DrawShip("tori")
@Charges({2: 1})
class ShipC(Thing):
	letter = "C"

# Buildings

@DrawName()
@HasPad(4)
@Rechargeable({0: 10})
@Discharges()
@RevealsOnCharge(25)
class Building(Thing):
	brange = 30

@DrawName()
@HasPad(4)
@Rechargeable({0: 100, 1: 100, 2: 100})
class ObjectiveQTower(Thing):
	brange = 50

@DrawName()
@HasPad(10)
@TracksProximity()
class ObjectiveX(Thing):
	brange = 50

@DrawName()
@HasPad(4)
@Discharges()
@Rechargeable({0: 20, 1: 20, 2: 20})
class ObjectiveXTower(Thing):
	brange = 50


# Effects

@Lifetime(0.7)
@DrawEllipses(r = 5)
class GoIndicator(Thing):
	pass

@SeverableConnection()
@SeversOnCharge()
@DrawChargeEffect()
class ChargeEffect(Thing):
	pass

@DrawBallLightning()
class BallLightning(Thing):
	pass

@Lifetime(0.6)
@NeedColored()
@DrawShakyConnection(thick = 3)
class NeedConnector(Thing):
	pass

@Lifetime(1.7)
@DrawEllipses(r = 30, width = 3)
@NeedColored()
class NeedIndicator(Thing):
	pass

@DrawSmoke()
class Smoke(Thing):
	pass


# Decorations

@DrawName()
class Tree(Thing):
	pass


