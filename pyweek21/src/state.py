import cPickle as pickle
from . import settings, window

class State(object):
	def __init__(self):
		self.ships = []
		self.buildings = []

	def draw(self):
		for t in self.ships + self.buildings:
			t.draw()

	def think(self, dt):
		for t in self.ships + self.buildings:
			t.think(dt)

	def get(self):
		return [
			window.getstate(),
			self.ships,
			self.buildings,
		]

	def set(self, obj):
		[
			windowstate,
			self.ships,
			self.buildings
		] = obj
		window.setstate(windowstate)


state = State()

def save():
	pickle.dump(state.get(), open(settings.savename, "wb"))

def load():
	global state
	state.set(pickle.load(open(settings.savename, "rb")))

