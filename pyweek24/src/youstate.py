# State machine for the player character

# The player character (you) at any given time has a state (you.state) that controls certain
# behavior. This is confusingly named, as it's separate from the state module, which controls the
# overall state of the game objects.

# Player state classes are never instantiated. They have static methods that act on the player
# object (referred to as self).

import pygame, math
from . import enco, state, view, pview, settings, drawyou

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
	def draw(self):
		pass
	@staticmethod
	def exit(self):
		pass
	@staticmethod
	def gethit(self):
		pass

class Falling(BaseState):
	@staticmethod
	def enter(self):
		self.tprejump = 0
		self.prejumping = False
		self.slowfall = True
	@staticmethod
	def control(self, kdowns, kpressed):
		if settings.isdown(kdowns, "jump"):
			self.prejumping = True
			self.tprejump = 0
		if settings.DEBUG and pygame.K_BACKSPACE in kdowns:
			self.enterstate(Dying)
		self.slowfall = settings.ispressed(kpressed, "jump")
		if self.prejumping and not settings.isdown(kdowns, "jump"):
			self.prejumping = False
			self.tprejump = 0
	@staticmethod
	def think(self, dt):
		a = 60 if self.slowfall else 160
		self.y += self.vy * dt - 0.5 * a * dt ** 2
		self.vy -= a * dt
		vx = state.youtargetspeed()
		self.x += vx * dt
		if self.prejumping:
			self.tprejump += dt
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
		if self.prejumping and self.tprejump < settings.prejumptime:
			self.vy = 30
			self.enterstate(Falling)
	@staticmethod
	def draw(self):
		drawyou.falling(self.screenpos(), 8 * pview.f, self.vy)
	@staticmethod
	def gethit(self):
		self.enterstate(Dying)

class Running(BaseState):
	@staticmethod
	def runspeed(self):
		vx = state.youtargetspeed()
		slopefactor = 1 - 0.5 * self.parent.slope
		slopefactor = max(slopefactor, 0.25)
		vx *= slopefactor
		return vx
	@staticmethod
	def enter(self, parent, a):
		self.parent = parent
		self.boarda = a
		self.tdraw = 0
		self.cliffhanging = False
		self.vx = Running.runspeed(self)
	@staticmethod
	def control(self, kdowns, kpressed):
		if settings.isdown(kdowns, "jump"):
			tcliff = (1 - self.boarda) * self.parent.d0 / self.vx
			cancliffhang = tcliff < settings.cliffhangtime and self.parent.handoff() is None
			if cancliffhang:
				self.cliffhanging = True
			else:
				self.vy = 30
				self.enterstate(Falling)
		if settings.DEBUG and pygame.K_BACKSPACE in kdowns:
			self.enterstate(Dying)
		if self.cliffhanging and not settings.isdown(kdowns, "jump"):
			self.vy = 30
			self.enterstate(Falling)
	@staticmethod
	def think(self, dt):
		vx = Running.runspeed(self)
		self.vx = math.approach(self.vx, vx, 10 * dt)
		self.boarda += vx * dt / self.parent.d
		self.tdraw += 2 * dt * vx / settings.speed
		self.tdraw %= 1
	@staticmethod
	def resolve(self):
		if not 0 <= self.boarda or self.parent.blockedat(self.boarda):
			self.enterstate(Falling)
			self.vy = 30 if self.cliffhanging else 0
			return
		if not self.boarda < 1:
			if self.cliffhanging:
				self.vy = 30
				self.enterstate(Falling)
			else:
				nextparent = self.parent.handoff()
				if nextparent is None:
					self.enterstate(Falling)
					self.vy = 0
					return
				self.parent = nextparent
				self.boarda -= 1
		self.x, self.y = view.to0(*self.parent.along(self.boarda))
		return

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
	@staticmethod
	def draw(self):
		drawyou.running(self.screenpos(), 8 * pview.f, self.tdraw)
	@staticmethod
	def gethit(self):
		self.enterstate(Dying)

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
	@staticmethod
	def draw(self):
		drawyou.falling(self.screenpos(), 8 * pview.f, self.vy)

class YouStates(enco.Component):
	def setstate(self, state = Falling, **args):
		self.state = None
		self.state = state
		self.vy = 10
		self.state.enter(self)
	def control(self, kdowns, kpressed):
		self.state.control(self, kdowns, kpressed)
	def think(self, dt):
		self.state.think(self, dt)
	def draw(self):
		self.state.draw(self)
	def resolve(self):
		self.state.resolve(self)
	def enterstate(self, state, *args, **kw):
		if self.state is not None:
			self.state.exit(self)
		self.state = state
		self.state.enter(self, *args, **kw)
		self.think(0)
	def gethit(self):
		self.state.gethit(self)



