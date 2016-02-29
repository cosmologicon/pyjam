from __future__ import division
import math, random
import cPickle as pickle
from collections import defaultdict
from . import settings, window

class State(object):
	def __init__(self):
		self.ships = []
		self.team = []
		self.buildings = []
		self.blocks = defaultdict(list)
		self.effects = []

	def assemble(self, x, y):
		team = sorted(self.team, key = lambda ship: (ship.x - x) ** 2 + (ship.y - y) ** 2)
		for j, ship in enumerate(team, 1):
			r, theta = 2 * math.sqrt(j), 1.62 * j
			ship.x = x + r * math.sin(theta)
			ship.y = y + r * math.cos(theta) - 3
			ship.target = None
			ship.btarget = None
		window.snaptopos(x, y, 0)

	def draw(self):
		for t in self.ships:
			t.drawshadow()
		things = self.ships + self.buildings + self.effects
		things.sort(key = lambda obj: -obj.y * window.fz + obj.z * window.fy)
		for t in things:
			t.draw()

	def think(self, dt):
		for t in self.ships + self.buildings + self.effects:
			t.think(dt)
		self.effects = [e for e in self.effects if e.alive]

	def addtoteam(self, ship):
		self.ships.append(ship)
		self.team.append(ship)

	def addbuilding(self, building):
		bx0 = int(math.floor((building.x - building.brange) / settings.blocksize))
		by0 = int(math.floor((building.y - building.brange) / settings.blocksize))
		bx1 = int(math.ceil((building.x + building.brange) / settings.blocksize)) + 1
		by1 = int(math.ceil((building.y + building.brange) / settings.blocksize)) + 1
		for bx in range(bx0, bx1):
			for by in range(by0, by1):
				self.blocks[(bx, by)].append(building)
		self.buildings.append(building)

	def buildingsnear(self, x, y):
		bx = int(x / settings.blocksize)
		by = int(y / settings.blocksize)
		return self.blocks[(bx, by)]

	def get(self):
		from . import quest, dialogue
		return [
			window.getstate(),
			quest.quests,
			dialogue.played,
			self.ships,
			self.team,
			self.buildings,
		]

	def set(self, obj):
		from . import quest
		[
			windowstate,
			quest.quests,
			dialogue.played,
			self.ships,
			self.team,
			buildings,
		] = obj
		window.setstate(windowstate)
		for building in buildings:
			self.addbuilding(building)


state = State()

def save():
	pickle.dump(state.get(), open(settings.savename, "wb"))

def load():
	global state
	state.set(pickle.load(open(settings.savename, "rb")))

