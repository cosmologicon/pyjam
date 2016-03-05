from __future__ import division
import math, random, os
try:
	import cPickle as pickle
except ImportError:
	import pickle
from collections import defaultdict
from . import settings, window, sound

class State(object):
	def __init__(self):
		self.ships = []
		self.team = []
		self.buildings = []
		self.blocks = defaultdict(list)
		self.effects = []
		self.decorations = []
		self.dblocks = defaultdict(list)
		self.bank = 0

	def assemble(self, x, y):
		team = sorted(self.team, key = lambda ship: (ship.x - x) ** 2 + (ship.y - y) ** 2)
		for j, ship in enumerate(team, 1):
			r, theta = 10 * math.sqrt(j), 1.62 * j
			ship.x = x + r * math.sin(theta)
			ship.y = y + r * math.cos(theta) - 3
			ship.target = None
			ship.btarget = None
		window.snaptopos(x, y, 0)

	def draw(self):
		for t in self.ships:
			if t.revealed():
				t.drawshadow()
		things = self.ships + self.buildingsnear(window.x0, window.y0) + self.effects + self.decorationsnear()
		things.sort(key = lambda obj: -obj.y * window.fz + obj.z * window.fy)
		for t in things:
			t.draw()
		for b in self.buildings:
			if hasattr(b, "drawbolt"):
				b.drawbolt()

	def think(self, dt):
		for t in self.ships + self.buildings + self.effects:
			t.think(dt)
		self.effects = [e for e in self.effects if e.alive]

	def addtoteam(self, ship):
		if ship not in self.ships:
			self.ships.append(ship)
		self.team.append(ship)

	def addbuilding(self, building):
		r = max(building.brange, 1.1 * settings.resolution0 / window.Z)
		bx0 = int(math.floor((building.x - r) / settings.blocksize))
		by0 = int(math.floor((building.y - r) / settings.blocksize))
		bx1 = int(math.ceil((building.x + r) / settings.blocksize)) + 1
		by1 = int(math.ceil((building.y + r) / settings.blocksize)) + 1
		for bx in range(bx0, bx1):
			for by in range(by0, by1):
				self.blocks[(bx, by)].append(building)
		self.buildings.append(building)


	def adddecoration(self, decoration):
		drange = 100
		bx0 = int(math.floor((decoration.x - drange) / settings.blocksize))
		by0 = int(math.floor((decoration.y - drange) / settings.blocksize))
		bx1 = int(math.ceil((decoration.x + drange) / settings.blocksize)) + 1
		by1 = int(math.ceil((decoration.y + drange) / settings.blocksize)) + 1
		for bx in range(bx0, bx1):
			for by in range(by0, by1):
				self.dblocks[(bx, by)].append(decoration)
		self.decorations.append(decoration)

	def buildingsnear(self, x, y):
		bx = int(x / settings.blocksize)
		by = int(y / settings.blocksize)
		return self.blocks[(bx, by)]

	def decorationsnear(self):
		bx = int(window.x0 / settings.blocksize)
		by = int(window.y0 / settings.blocksize)
		return self.dblocks[(bx, by)]

	def reward(self, amount):
		sound.play("reward")
		self.bank += amount

	def get(self):
		from . import quest, dialogue, background
		return [
			window.getstate(),
			background.getstate(),
			quest.quests,
			dialogue.played,
			self.ships,
			self.team,
			self.buildings,
			self.decorations
			self.bank,
		]

	def set(self, obj):
		self.__init__()
		from . import quest, dialogue, background
		[
			windowstate,
			backgroundstate,
			quest.quests,
			dialogue.played,
			self.ships,
			self.team,
			buildings,
			decorations,
			self.bank,
		] = obj
		window.setstate(windowstate)
		background.setstate(backgroundstate)
		for building in buildings:
			self.addbuilding(building)
		for decoration in decorations:
			self.adddecoration(decoration)


state = State()

def save():
	pickle.dump(state.get(), open(settings.savename, "wb"))

def load():
	global state
	state.set(pickle.load(open(settings.savename, "rb")))

def deletesave():
	if os.path.exists(settings.savename):
		os.remove(settings.savename)

