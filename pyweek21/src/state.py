import cPickle as pickle
from . import settings, thing

class State(object):
	def __init__(self):
		self.things = []

	def draw(self):
		for t in self.things:
			t.draw()

	def think(self, dt):
		for t in self.things:
			t.think(dt)

	def get(self):
		return [
			window.getstate(),
			self.things,
		]

	def set(self, obj):
		[
			windowstate,
			self.things,
		] = obj
		window.setstate(windowstate)


state = State()

def save():
	pickle.dump(state.get(), open(settings.savename, "wb"))

def load():
	global state
	state.set(pickle.load(open(settings.savename, "rb")))

