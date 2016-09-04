import pygame, math
from . import view, control, state
from .util import F
from .enco import Component

class Lives(Component):
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

class Mouseable(Component):
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
			control.cursor = self
	def ondrag(self, pos):
		if self is control.cursor:
			self.x, self.y = pos

class DrawCircle(Component):
	def setstate(self, r = 10, color = (100, 0, 0), **kw):
		self.r = r
		self.color = color
	def draw(self):
		pygame.draw.circle(view.screen, self.color, view.screenpos((self.x, self.y)), view.screenlength(self.r))

class DisappearsToCenter(Component):
	def setstate(self, approaching = False, **kw):
		self.approaching = approaching
	def onhover(self):
		self.preserved = True
		self.approaching = True
	def think(self, dt):
		if not self.approaching or not self.alive:
			return
		d = math.sqrt(self.x ** 2 + self.y ** 2)
		D = dt * 100
		if D > d:
			self.x = self.y = 0
			self.arrive()
		else:
			self.x -= self.x * D / d
			self.y -= self.y * D / d
	def arrive(self):
		self.die()

class GetsATP(Component):
	def arrive(self):
		state.atp += 1

@Lives()
@WorldBound()
@DrawCircle()
class Amoeba(object):
	def __init__(self, **kw):
		self.setstate(**kw)

@Lives()
@Lifetime()
@WorldBound()
@Mouseable()
@DisappearsToCenter()
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
@Mouseable()
@Draggable()
@DrawCircle()
class Organelle(object):
	def __init__(self, **kw):
		self.setstate(
			color = (250, 120, 0),
			r = 6, rmouse = 6,
			**kw)


