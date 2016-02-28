import math
import cPickle as pickle
from collections import defaultdict
from . import settings, window

class State(object):
	def __init__(self):
		self.ships = []
		self.team = []
		self.buildings = []
		self.blocks = defaultdict(list)
		self.cursor = None

	def nextcursor(self):
		if not self.cursor:
			return self.team[0]
		return self.team[(self.team.index(self.cursor) + 1) % len(self.team)]

	def draw(self):
		for t in self.ships:
			t.drawshadow()
		things = self.ships + self.buildings
		things.sort(key = lambda obj: -obj.y * window.fz + obj.z * window.fy)
		for t in things:
			t.draw()

	def think(self, dt):
		for t in self.ships + self.buildings:
			t.think(dt)

	def addtoteam(self, ship):
		self.ships.append(ship)
		self.team.append(ship)

	def addbuilding(self, building):
		bx0 = int(math.floor((building.x - building.brange) / settings.blocksize))
		by0 = int(math.floor((building.y - building.brange) / settings.blocksize))
		bx1 = int(math.ceil((building.x + building.brange) / settings.blocksize))
		by1 = int(math.ceil((building.y + building.brange) / settings.blocksize))
		for bx in range(bx0, bx1):
			for by in range(by0, by1):
				self.blocks[(bx, by)].append(building)
		self.buildings.append(building)

	def buildingsnear(self, x, y):
		bx = int(x / settings.blocksize)
		by = int(y / settings.blocksize)
		return self.blocks[(bx, by)]

	def get(self):
		return [
			window.getstate(),
			self.ships,
			self.team,
			self.buildings,
		]

	def set(self, obj):
		[
			windowstate,
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

