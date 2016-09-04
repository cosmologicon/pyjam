import pygame, math, random
from . import view, control, state, blob, img, settings, bounce
from .util import F
from .enco import Component

class Lives(Component):
	def addtostate(self):
		state.thinkers.append(self)
	def setstate(self, alive = True, t = 0, **kw):
		self.alive = alive
		self.t = t
	def think(self, dt):
		self.t += dt
	def die(self):
		self.alive = False

class Lifetime(Component):
	def setstate(self, lifetime = 1, preserved = False, **kw):
		self.lifetime = lifetime
		self.flife = math.clamp(self.t / self.lifetime, 0, 1)
		self.preserved = preserved
	def think(self, dt):
		if not self.alive:
			return
		self.flife = math.clamp(self.t / self.lifetime, 0, 1)
		if self.t > self.lifetime and not self.preserved:
			self.die()

class WorldBound(Component):
	def setstate(self, x = 0, y = 0, **kw):
		self.x = x
		self.y = y
	def scootch(self, dx, dy):
		self.x += dx
		self.y += dy

class Drawable(Component):
	def addtostate(self):
		state.drawables.append(self)

class Collidable(Component):
	def setstate(self, rcollide = 10, mass = 10, **kw):
		self.rcollide = rcollide
		self.mass = mass
	def getcollidespec(self):
		return self.x, self.y, self.rcollide, self.mass
	def draw(self):
		if settings.showbox:
			pygame.draw.circle(view.screen, (255, 255, 255),
				view.screenpos((self.x, self.y)), view.screenlength(self.rcollide), 1)

class WorldCollidable(Collidable):
	def addtostate(self):
		state.colliders.append(self)

class Mouseable(Component):
	def addtostate(self):
		state.mouseables.append(self)
	def setstate(self, rmouse = 5, **kw):
		self.rmouse = rmouse
	def within(self, pos):
		x, y = pos
		return (x - self.x) ** 2 + (y - self.y) ** 2 < self.rmouse ** 2
	def onhover(self):
		pass
	def ondrag(self, pos):
		pass
	def onmousedown(self):
		pass

class Draggable(Component):
	def onmousedown(self):
		if control.cursor is None:
			if len(self.container.slots) == 1 and self.container.mass < 9999:
				control.cursor = self.container
			else:
				self.container.remove(self)
				control.cursor = self.totower()
			state.removeobj(control.cursor)

class DrawCircle(Component):
	def setstate(self, r = 10, color = (100, 0, 0), **kw):
		self.r = r
		self.color = color
	def draw(self):
		pygame.draw.circle(view.screen, self.color, view.screenpos((self.x, self.y)), view.screenlength(self.r))
	def drawback(self):
		pass

class DrawVirus(Component):
	def setstate(self, r = 10, **kw):
		self.r = r
		self.tdraw0 = random.uniform(0, 1000)
	def draw(self):
		tdraw = self.tdraw0 + self.t
		fstretch = math.exp(0.3 * math.sin(10 * tdraw))
		angle = 15 * math.sin(0.6 * tdraw)
		dy = 0.3 * self.r * math.sin(10 * tdraw)
		img.drawworld("virus", (self.x, self.y + dy), self.r, fstretch = fstretch, angle = angle)
	def drawback(self):
		pass

class DrawBlob(Component):
	def setstate(self, rblob = 10, nblob = 3, **kw):
		self.rblob = rblob
		self.nblob = nblob
		self.blobspecs = [(
			random.uniform(0, math.tau),
			random.uniform(0.6, 1) * (-1 if j % 2 else 1),
			random.uniform(0.6, 0.8),
		) for j in range(self.nblob)]
	def draw(self):
		pass
	def drawback(self):
		img = blob.hill(view.screenlength(2 * self.rblob), 1)
		view.blobscreen.blit(img, img.get_rect(center = view.screenpos((self.x, self.y))))
		for theta0, dtheta, fr in self.blobspecs:
			theta = theta0 + self.t * dtheta
			x = self.x + fr * self.rblob * math.sin(theta)
			y = self.y + fr * self.rblob * math.cos(theta)
			img = blob.hill(view.screenlength(0.8 * self.rblob), 0.5)
			view.blobscreen.blit(img, img.get_rect(center = view.screenpos((x, y))))

class Hatches(Component):
	def die(self):
		if self not in self.container.slots:
			return
		organelle = Organelle(flavor = self.flavor, container = self.container, x = self.x, y = self.y)
		self.container.remove(self)
		self.container.add(organelle)
		organelle.addtostate()

class HasSlots(Component):
	def setstate(self, slots = None, nslot = 3, **kw):
		self.slots = slots or []
		self.nslot = nslot
	def isfull(self):
		return len(self.slots) >= self.nslot
	def add(self, obj):
		self.slots.append(obj)
	def remove(self, obj):
		self.slots.remove(obj)
	def think(self, dt):
		f = 1 - math.exp(-dt)
		for obj in self.slots:
			obj.x += (self.x - obj.x) * f
			obj.y += (self.y - obj.y) * f
		if len(self.slots) > 1:
			bounce.adjust(self.slots, dt)
	def scootch(self, dx, dy):
		for obj in self.slots:
			obj.scootch(dx, dy)

class Buildable(Component):
	def addtostate(self):
		state.buildables.append(self)
	def cantake(self, obj):
		if len(obj.slots) + len(self.slots) > self.nslot:
			return False
		dx, dy = obj.x - self.x, obj.y - self.y
		r = self.rcollide + obj.rcollide
		return dx ** 2 + dy ** 2 < r ** 2

class ResizesWithSlots(Component):
	def add(self, obj):
		self.resize()
	def remove(self, obj):
		self.resize()
	def resize(self):
		self.mass = 4
		# TODO: better resizing algorithm
		if self.slots:
			r = sum(obj.rcollide ** 1.8 for obj in self.slots) ** (1/1.8)
			self.mass += sum(obj.mass for obj in self.slots)
		else:
			r = 4
		self.rcollide = r
		self.rblob = r

# Move from p0 to p1 by an amount d, and return if you've arrived
def approachpos(p0, p1, d):
	x0, y0 = p0
	x1, y1 = p1
	dx, dy = x1 - x0, y1 - y0
	dp = math.sqrt(dx ** 2 + dy ** 2)
	if dp < d:
		return x1, y1, True
	return x0 + dx * d / dp, y0 + dy * d / dp, False

class DisappearsToCenter(Component):
	def setstate(self, approaching = False, **kw):
		self.approaching = approaching
	def onhover(self):
		self.preserved = True
		self.approaching = True
	def think(self, dt):
		if not self.approaching or not self.alive:
			return
		self.x, self.y, arrived = approachpos((self.x, self.y), (0, 0), dt * 100)
		if arrived:
			self.arrive()

class TargetsThing(Component):
	def setstate(self, target = None, speed = 10, **kw):
		self.target = target
		self.speed = speed
	def think(self, dt):
		if self.alive and self.target is not None:
			self.x, self.y, arrived = approachpos((self.x, self.y), (self.target.x, self.target.y), self.speed * dt)
			if arrived:
				self.arrive()

class DiesOnArrival(Component):
	def arrive(self):
		self.die()

class HarmsOnArrival(Component):
	def arrive(self):
		state.health -= 1

class GetsATP(Component):
	def arrive(self):
		state.atp += 1

@Lives()
@WorldBound()
@Drawable()
@DrawBlob()
@HasSlots()
@Buildable()
@WorldCollidable()
class Amoeba(object):
	def __init__(self, **kw):
		self.setstate(
			rcollide = 20, mass = 10000,
			rblob = 20,
			nblob = 18,
		**kw)

@Lives()
@WorldBound()
@Drawable()
@DrawBlob()
@HasSlots()
@Buildable()
@ResizesWithSlots()
@WorldCollidable()
class Tower(object):
	def __init__(self, **kw):
		self.setstate(
			rcollide = 20, mass = 10,
			rblob = 20,
			nblob = 18,
		**kw)

@Lives()
@Lifetime()
@WorldBound()
@Drawable()
@Mouseable()
@DisappearsToCenter()
@DiesOnArrival()
@DrawCircle()
@GetsATP()
class ATP(object):
	def __init__(self, **kw):
		self.setstate(
			color = (200, 200, 0),
			r = 4, rmouse = 4,
			lifetime = 5,
			**kw)

@Lives()
@WorldBound()
@Drawable()
@Mouseable()
@Draggable()
@DrawBlob()
@DrawCircle()
@Collidable()
class Organelle(object):
	def __init__(self, flavor, container, x = None, y = None, **kw):
		color = {
			0: (255, 0, 0),
			1: (0, 255, 0),
			2: (100, 100, 255),
		}[flavor]
		self.container = container
		if x is None:
			x = container.x + random.uniform(-1, 1)
		if y is None:
			y = container.y + random.uniform(-1, 1)
		self.setstate(
			rcollide = 6, mass = 10,
			rblob = 6, rmouse = 6,
			nblob = 0,
			r = 6, color = color,
			x = x, y = y,
			**kw)
		self.flavor = flavor
	def totower(self):
		tower = Tower(x = self.x, y = self.y)
		tower.add(self)
		self.container = tower
		return tower



@Lives()
@Lifetime()
@WorldBound()
@Drawable()
@DrawCircle()
@Collidable()
@Hatches()
class Egg(object):
	def __init__(self, flavor, container, **kw):
		self.container = container
		color = {
			0: (255, 0, 0, 120),
			1: (0, 255, 0, 120),
			2: (100, 100, 255, 120),
		}[flavor]
		self.setstate(
			r = 8, color = color,
			lifetime = 3,
			x = container.x + random.uniform(-1, 1),
			y = container.y + random.uniform(-1, 1),
			**kw)
		self.flavor = flavor

@Lives()
@WorldBound()
@Drawable()
@TargetsThing()
@DiesOnArrival()
@HarmsOnArrival()
@DrawVirus()
@WorldCollidable()
class Virus(object):
	def __init__(self, **kw):
		self.setstate(
			speed = random.uniform(4, 6),
			rcollide = 6, mass = 5,
			r = 6, color = (255, 255, 255),
			**kw)


