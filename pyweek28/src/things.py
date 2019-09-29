# Game entities

from __future__ import division
import pygame, random, math
from . import pview, view, quest, state, draw, ptext, sound
from .lru_cache import lru_cache
from .pview import T

popnames = {
	"worker": "Workazoid",
	"tech": "Technoton",
	"sci": "Calculax",
	"porter": "Porton",
	"fixer": "Repairzo",
}


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
	def wantscar(self):
		return self.htargets and isinstance(self.holder, Station) and isinstance(self.htargets[0], Station)
	def think(self, dt):
		if self.wantscar() and 0.2 * random.random() < dt:
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
def getpopcard(name, color, size, alpha = 255):
	if alpha != 255:
		surf = getpopcard(name, color, size).copy()
		osurf = pygame.Surface(surf.get_size()).convert_alpha()
		osurf.fill((255, 225, 255, alpha))
		surf.blit(osurf, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
		return surf
	if size != 120:
		return pygame.transform.smoothscale(getpopcard(name, color, 120), (size, size))
	surf = pygame.Surface((120, 120)).convert_alpha()
	surf.fill(color)
	surf.fill(math.imix((0, 0, 0), color, 0.5), (6, 6, 108, 108))
	if name:
		fname = {
			"worker": "16",
			"sci": "33",
			"tech": "24",
			"porter": "26",
			"fixer": "7",
		}[name]
		img = pygame.image.load("img/%s.png" % fname).convert_alpha()
		surf.blit(pygame.transform.smoothscale(img, (120, 120)), (0, 0))
#		ptext.draw(name[0].upper(), surf = surf, center = (60, 60), fontsize = 100, owidth = 1.5)
		ptext.draw(popnames[name], surf = surf, center = (60, 96), fontsize = 30, owidth = 1.5)
	return surf

# Member of the population, a person
class Pop(Passenger):
	def __init__(self, name, holder = None):
		Passenger.__init__(self, holder)
		self.name = name
	def color(self):
		if self.name == "worker": return 100, 100, 255
		if self.name == "tech": return 255, 100, 100
		if self.name == "sci": return 255, 255, 0
		if self.name == "porter": return 200, 200, 200
		if self.name == "fixer": return 100, 100, 100
	def getcard(self, size, fade = 1, alpha = 255):
		color = math.imix((0, 0, 0), self.color(), fade)
		return getpopcard(self.name, color, size, alpha)
	def drawcard(self, pos, size, fade = 1, alpha = 255):
		surf = self.getcard(size, fade, alpha)
		rect = surf.get_rect(center = pos)
		pview.screen.blit(surf, rect)
		if self.wantscar():
			t = int(0.002 * pygame.time.get_ticks())
			for j in [0, 5, 20]:
				x0 = math.phi * (t + j) % 1
				y0 = (math.phi * (t + j) ** 2 + 0.6) % 1
				ptext.draw("?", center = pview.I(pos[0] + size * (x0 - 0.5) / 2, pos[1] + size * (y0 - 0.5) / 2),
					fontsize = T(size / 2), owidth = 1)
		if self.htargets:
			ptext.draw(self.htargets[-1].name[0], topright = rect.topright, fontsize = T(size/2), owidth = 1)

def drawemptycard(pos, size):
	surf = getpopcard("", (60, 60, 60), size, 50)
	rect = surf.get_rect(center = pos)
	pview.screen.blit(surf, rect)


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
		self.mission = None
		self.t = 0
		self.blocked = [self.portcapacity() < 8 for _ in range(8)]
		self.unblockseq = [A for A in range(8)]
	def toggleblock(self, A):
		if not self.blocked[A]:
			self.blocked[A] = True
			sound.playsound("machine_off")
		else:
			capacity = self.portcapacity()
			nopen = sum(not b for b in self.blocked)
			if nopen < capacity:
				canunblock = True
			elif nopen == capacity:
				bA = self.toblock()
				if bA is None:
					canunblock = False
				else:
					self.blocked[bA] = True
					canunblock = True
			else:
				canunblock = False
			if canunblock:
				self.blocked[A] = False
				sound.playsound("machine_on")
				if A in self.unblockseq:
					self.unblockseq.remove(A)
				self.unblockseq.append(A)
			else:
				sound.playsound("no")
	def portcapacity(self):
		if self.name == "Ground Control":
			return 8
		if any(held.name == "porter" for held in self.held):
			return 8
		return state.portcapacity[min(len(self.held), len(state.portcapacity))]
	def toblock(self):
		for A in self.unblockseq:
			if self.blocked[A] or self.portinuse(A):
				continue
			return A
		return None
	def portinuse(self, A):
		return any(car.A == A and self in car.stationtargets() for car in state.cars)
	def showncapacity(self):
		# If unlimited capacity (i.e. over 100000), show just the current occupants
		return self.capacity if self.capacity < 100000 else len(self.held) + len(self.pending)
	def addquest(self, questname):
		self.quests.append(questname)
	def startquest(self, questname):
		self.quests.remove(questname)
		quest.start(questname)
	def setmission(self, need, reward):
		self.mission = quest.MissionQuest(self, need, reward)
		quest.start(self.mission)
	def think(self, dt):
		self.t += dt
		capacity = self.portcapacity()
		while sum(not b for b in self.blocked) > capacity and self.toblock() is not None:
			self.blocked[self.toblock()] = True
	def especs(self):
		if not view.visible(self.z, 10):
			return []
		return [
			(texturename, xW, yW, self.z + zW0, self.z + zW1, r0, r1, n, dA, k)
			for texturename, xW, yW, zW0, zW1, r0, r1, n, dA, k in
			stationespecs(self.name, self.t)
		]

class Car(Holder):
	name = None
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
		sound.playsound("clang%d" % random.choice([0, 1, 2, 3]))
		if random.random() < 1/3:
			self.broken = False
		self.fjostle = 1
	def cantransport(self, zfrom, zto):
		if not self.canaddpassenger(): return False
		return not any(state.stationat(z).blocked[self.A] for z in (zfrom, zto))
	def stationtargets(self):
		stations = [s for p in self.pending for s in p.htargets if isinstance(s, Station)]
		if self.targetz:
			stations.append(state.stationat(self.targetz))
		return stations
	def think(self, dt):
		if state.progress.missions >= 3 and 15 * random.random() < dt and abs(self.targetz - self.z) > 500:
#		if 20 * random.random() < dt:
			self.broken = True
		if self.broken:
			s = state.stationat(self.z)
			if s and any(p.name == "fixer" for p in s.held):
				self.broken = False
		self.fjostle = math.approach(self.fjostle, 0, 1.5 * dt)
		self.brokefactor = math.approach(self.brokefactor, (4 if self.broken else 1), 3 * dt)
		dt *= 1 + state.progress.carupgrades
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

# Espec: texturename, xW, yW, zW0, zW1, r0, r1, n, dA, k
def stationespecs(name, t):
	dA = 0.1 * t
	if name == "Ground Control":
		return [
			["roundtop", 0, 0, -2, 3, 4, 2, 0.2, 0, 10],
			["stripe-orange", 0, 0, 1, 1.3, 4, 4, 1, 0, 1],
		]
	if name == "Upzidazi":
		return [
			["lowwindow", 0, 0, -1.5, 1, 3, 3.5, 0.2, dA, 10],
			["lowwindow", 0, 0, 1, 4, 3.7, 4.2, 0.2, -0.6 * dA, 10],
			["rock", 0, 0, 4, 7, 4.2, 10, 0.1, 0, 3],
		]
	if name == "Flotogorb":
		ret = [
			["stripe-blue", x, y, (j-1) * 1 - 0.3, (j-1) * 1 + 0.3, 4, 4, 1, 0, 1]
			for j, (x, y) in enumerate(math.CSround(3, 2))
		] + [
			["solid-#666688", x, y, -5 + 2 * (j * math.phi % 1), 3 + 2 * (j * math.phi % 1), 0.2, 0.2, 1, 0, 1]
			for j, (x, y) in enumerate(math.CSround(6, 3))
		]
		return ret
	if name == "Skyburg":
		ret = [
			["roundtop", 0, 0, 0, 2, 5, 1, 7, 0, 12],
			["window", 0, 0, -1.2, 0, 2.5, 5, 0.2, 0, 18],
			["stripe-blue", 0, 0, -3, -1.2, 3.5, 2.5, 0.2, 0, 1],
		]
		return ret
	if name == "Lorbiton":
		ret = [
			["window", 0, 0, -2.4, 0, 1.5, 4.4, 1/10, 0, 12],
			["window", 0, 0, 0, 2.4, 4.4, 1.5, 10, 0, 12],
		]
		for (_, z), (x, y) in zip(math.CSround(3, 2, 2 * t), math.CSround(3, 4.5, 1.5 * t)):
			ret += [
				["gray", x, y, z, z + 0.5, 1, 0, 1/2, 0, 1],
				["gray", x, y, z - 0.5, z, 0, 1, 2, 0, 1],
			]
		for (_, z), (x, y) in zip(math.CSround(5, 2.5, 1 * t), math.CSround(5, 5, -1.1 * t)):
			ret += [
				["gray", x, y, z, z + 0.5, 1, 0, 1/2, 0, 1],
				["gray", x, y, z - 0.5, z, 0, 1, 2, 0, 1],
			]
		return ret
		
	specs = [
		["gray", 0, 0, -2, -0.7, 2, 4.2, 8, 0, 10],
		["hatch", 0, 0, -0.7, -0.5, 4.2, 4.2, 1, 0, 100],
		["window", 0, 0, -0.5, 0.5, 4, 4, 1, dA, 20],
		["hatch", 0, 0, 0.5, 0.7, 4.2, 4.2, 1, 0, 100],
		["gray", 0, 0, 0.7, 1.4, 4.2, 2, 8, 0, 10],
	]
	if name == "Ettiseek":
		for xW, yW in math.CSround(3, 3.5, 0.1234):
			specs.extend([
				["gray", xW, yW, -4.2, -2.2, 0.1, 0.1, 1, 0, 1],
				["gray", xW, yW, -2.2, -0.8, 0.2, 0.2, 1, 0, 1],
				["gray", xW, yW, 1, 2, 0.2, 0.2, 1, 0, 1],
				["gray", xW, yW, 2, 4, 0.1, 0.1, 1, 0, 1],
			])
	return specs

