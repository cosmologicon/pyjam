# State machine for the player character

# The player character (you) at any given time has a state (you.state) that controls certain
# behavior. This is confusingly named, as it's separate from the state module, which controls the
# overall state of the game objects.

# Player state classes are never instantiated. They have static methods that act on the player
# object (referred to as self).

import pygame
from . import enco, state, view, settings

class BaseState(object):
	@staticmethod
	def enter(self, *args, **kw):
		pass
	@staticmethod
	def control(self, kdowns, kpressed):
		pass
	@staticmethod
	def think(self, dt):
		pass
	@staticmethod
	def resolve(self):
		pass
	@staticmethod
	def exit(self):
		pass

class Falling(BaseState):
	@staticmethod
	def control(self, kdowns, kpressed):
		if pygame.K_SPACE in kdowns:
			self.vy = 20
		if settings.DEBUG and pygame.K_BACKSPACE in kdowns:
			self.enterstate(Dying)
	@staticmethod
	def think(self, dt):
		a = 50
		self.y += self.vy * dt - 0.5 * a * dt ** 2
		self.vy -= a * dt
		self.x += 12 * dt
	@staticmethod
	def resolve(self):
		catchers = []
		for boardname, a0, b0, a1, b1 in state.crossings:
			a = (a1 * b0 - a0 * b1) / (b0 - b1)
			if not 0 <= a < 1 or state.boards[boardname].blockedat(a):
				continue
			x, y = view.to0(*state.boards[boardname].along(a))
			catchers.append((y, boardname, a))
		if not catchers:
			return
		y, boardname, a = max(catchers)
		self.enterstate(Running, state.boards[boardname], a)

class Running(BaseState):
	@staticmethod
	def enter(self, parent, a):
		self.parent = parent
		self.boarda = a
	@staticmethod
	def control(self, kdowns, kpressed):
		if pygame.K_SPACE in kdowns:
			self.vy = 20
			self.enterstate(Falling)
		if settings.DEBUG and pygame.K_BACKSPACE in kdowns:
			self.enterstate(Dying)
	@staticmethod
	def think(self, dt):
		self.boarda += 12 * dt / self.parent.d
	@staticmethod
	def resolve(self):
		if not 0 <= self.boarda < 1:
			self.enterstate(Falling)
			self.vy = 0
			return
		if self.parent.blockedat(self.boarda):
			self.enterstate(Falling)
			self.vy = 0
			return
		self.x, self.y = view.to0(*self.parent.along(self.boarda))
		catchers = [(self.y, self.parent.name, self.boarda)]
		for boardname, a0, b0, a1, b1 in state.crossings:
			a = (a1 * b0 - a0 * b1) / (b0 - b1)
			if not 0 <= a < 1 or state.boards[boardname].blockedat(a):
				continue
			x, y = view.to0(*state.boards[boardname].along(a))
			catchers.append((y, boardname, a))
		if len(catchers) == 1:
			return
		y, boardname, a = max(catchers)
		if boardname != self.parent.name:
			self.enterstate(Running, state.boards[boardname], a)

class Dying(BaseState):
	@staticmethod
	def enter(self):
		self.vy = 20
		self.vx = -2
	@staticmethod
	def think(self, dt):
		a = 100
		self.y += self.vy * dt - 0.5 * a * dt ** 2
		self.vy -= a * dt
		self.x += self.vx * dt

class YouStates(enco.Component):
	def setstate(self, state = Falling, **args):
		self.state = state
		self.vy = 10
	def control(self, kdowns, kpressed):
		self.state.control(self, kdowns, kpressed)
	def think(self, dt):
		self.state.think(self, dt)
	def resolve(self):
		self.state.resolve(self)
	def enterstate(self, state, *args, **kw):
		self.state.exit(self)
		self.state = state
		self.state.enter(self, *args, **kw)


