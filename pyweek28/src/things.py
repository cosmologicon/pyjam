# Game entities

from __future__ import division
import pygame, random, math
from functools import lru_cache
from . import pview, view, quest, state, draw, ptext
from .pview import T

# Base class for all kinds of passengers/inhabitants of a car or station.
class Passenger:
	def __init__(self, holder = None):
		self.htargets = []
		self.holder = None  # The car or station where this passenger is.
		self.setholder(holder)
	def color(self):
		return 120, 255, 120
	def setholder(self, holder):
		if self.holder is not None:
			self.holder.removepassenger(self)
		self.holder = holder
		if self.holder is not None:
			self.holder.addpassenger(self)
		while self.htargets and self.htargets[0] is self.holder:
			self.htargets.pop(0)
	def settargetholder(self, target):
		for htarget in self.htargets:
			if self in htarget.pending:
				htarget.pending.remove(self)
		self.htargets = [target]
		target.pending.append(self)
	def think(self, dt):
		if self.htargets:
			if isinstance(self.holder, Station) and isinstance(self.htargets[0], Station):
				if 0.2 * random.random() < dt:
					self.callcar()
		if self.htargets and self.holder.z == self.htargets[0].z:
			self.setholder(self.htargets[0])
		if self.htargets and isinstance(self.holder, Car) and self.holder.targetz != self.htargets[0].z:
			self.holder.settarget(self.htargets[0].z)
	def callcar(self):
		cars = [car for car in state.cars if car.cantransport(self.holder.z, self.htargets[0].z)]
		if not cars:
			return
		car = min(cars, key = lambda car: abs(self.holder.z - car.z))
		self.htargets.insert(0, car)
		car.pending.append(self)

@lru_cache(1000)
def getpopcard(name, color, size):
	if size != 400:
		return pygame.transform.smoothscale(getpopcard(name, color, 400), (size, size))
	surf = pygame.Surface((400, 400)).convert_alpha()
	surf.fill(color)
	surf.fill(math.imix((0, 0, 0), color, 0.5), (20, 20, 360, 360))
	ptext.draw(name[0].upper(), surf = surf, center = (200, 200), fontsize = 360, owidth = 2)
	ptext.draw(name.title(), surf = surf, center = (200, 320), fontsize = 100, owidth = 1.5)
	return surf

# Member of the population, a person
class Pop(Passenger):
	def __init__(self, name, holder = None):
		Passenger.__init__(self, holder)
		self.name = name
	def color(self):
		if self.name == "worker": return 200, 150, 100
		if self.name == "tech": return 200, 200, 100
		if self.name == "sci": return 100, 200, 100
	def getcard(self, size, fade = 1):
		color = math.imix((0, 0, 0), self.color(), fade)
		return getpopcard(self.name, color, size)
	def drawcard(self, pos, size, fade = 1):
		surf = self.getcard(size, fade)
		rect = surf.get_rect(center = pos)
		pview.screen.blit(surf, rect)
		if self.htargets:
			ptext.draw(self.htargets[-1].name[0], topright = rect.topright, fontsize = T(size/2), owidth = 1)


class Holder:
	def __init__(self, capacity):
		self.capacity = capacity
		self.held = []
		self.pending = []
	def canaddpassenger(self, n = 1):
		return len(self.held) + len(self.pending) <= self.capacity - n
	def addpassenger(self, passenger):
		self.held.append(passenger)
		if passenger in self.pending:
			self.pending.remove(passenger)
	def removepassenger(self, passenger):
		self.held.remove(passenger)
	def recthelds(self):
		for j, held in enumerate(self.held):
			px, py = 50 + 80 * (j % 4), 330 + 80 * (j // 4)
			rect = T(pygame.Rect(0, 0, 72, 72))
			rect.center = T(px, py)
			yield rect, held

class Station(Holder):
	def __init__(self, name, z, capacity):
		Holder.__init__(self, capacity)
		self.name = name
		self.z = z
		self.messages = []
		self.quests = []
		self.t = 0
		self.blocked = [False for _ in range(8)]
	def addquest(self, questname):
		self.quests.append(questname)
	def startquest(self, questname):
		self.quests.remove(questname)
		quest.start(questname)
	def think(self, dt):
		self.t += dt
	def especs(self):
		if not view.visible(self.z, 10):
			return []
		dA = 0.1 * self.t
		specs = [
			["gray", 0, 0, self.z - 2, self.z - 0.7, 2, 4.2, 8, 0, 10],
			["hatch", 0, 0, self.z - 0.7, self.z - 0.5, 4.2, 4.2, 1, 0, 100],
			["window", 0, 0, self.z - 0.5, self.z + 0.5, 4, 4, 1, dA, 20],
			["hatch", 0, 0, self.z + 0.5, self.z + 0.7, 4.2, 4.2, 1, 0, 100],
			["gray", 0, 0, self.z + 0.7, self.z + 1.4, 4.2, 2, 8, 0, 10],
		]
		if self.name == "Last Ditch":
			for xW, yW in math.CSround(3, 3.5, 0.1234):
				specs.extend([
					["gray", xW, yW, self.z - 4.2, self.z - 2.2, 0.1, 0.1, 1, 0, 1],
					["gray", xW, yW, self.z - 2.2, self.z - 0.8, 0.2, 0.2, 1, 0, 1],
					["gray", xW, yW, self.z + 1, self.z + 2, 0.2, 0.2, 1, 0, 1],
					["gray", xW, yW, self.z + 2, self.z + 4, 0.1, 0.1, 1, 0, 1],
				])
		return specs

class Car(Holder):
	def __init__(self, z, A):
		Holder.__init__(self, capacity = 1)
		self.z = z
		self.A = A
		self.targetz = self.z
		self.vz = 0
		self.r = 0.8
		self.R = 1.3  # Distance from central axis
		# When a car nears its destination it switches to approach mode, which is exponential braking.
		self.braking = True
		self.broken = False
		self.brokefactor = 1
		self.fjostle = 0
	def arrived(self):
		return self.targetz == self.z
	def worldpos(self):
		yW, xW = math.CS(self.A/8 * math.tau, self.R)
		return xW, yW, self.z
	def tryfix(self):
		if not self.broken:
			return
		if random.random() < 1/3:
			self.broken = False
		self.fjostle = 1
	def cantransport(self, zfrom, zto):
		if not self.canaddpassenger(): return False
		return not any(state.stationat(z).blocked[self.A] for z in (zfrom, zto))
	def think(self, dt):
		self.fjostle = math.approach(self.fjostle, 0, 1.5 * dt)
		self.brokefactor = math.approach(self.brokefactor, (4 if self.broken else 1), 3 * dt)
		dt /= self.brokefactor
		if not self.arrived():
			b = 4  # braking factor. Set higher for shorter stops.
			brakez = math.softapproach(self.z, self.targetz, b * dt, dymin = 0.01)
			if not self.braking:
				self.vz += 200 * dt
				goz = math.approach(self.z, self.targetz, self.vz * dt)
				if abs(self.z - brakez) < abs(self.z - goz):
					self.braking = True
				else:
					self.z = goz
			if self.braking:
				self.vz = abs(brakez - self.z) / dt
				self.z = brakez
		if self.arrived and self.pending:
			self.settarget(self.pending[0].holder.z)
		if 100 * random.random() < dt:
			self.broken = True
	def settarget(self, zW):
		self.targetz = zW
		self.braking = False
	def especs(self):
		if not view.visible(self.z, 10):
			return []
		xW, yW, zW = self.worldpos()
		a = 0.1 * self.broken + 0.4 * self.fjostle
		if a:
			xW += random.uniform(-a, a)
			yW += random.uniform(-a, a)
			zW += random.uniform(-a, a)
		dA = pygame.time.get_ticks() * 0.00001
		specs = [
			["gray", xW, yW, zW - 1, zW + 1, 0.6, 0.6, 1, 0, 1],
			["window", xW, yW, zW - 0.7, zW + 0.7, 0.7, 0.7, 1, dA, 6],
		]
		return specs
