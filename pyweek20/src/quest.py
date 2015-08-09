from src import state, hud

quests = {}

# Quest data members need to be JSONable

class Quest(object):
	def __init__(self):
		quests[self.__class__.__name__] = self
		self.done = False
	def dump(self):
		return self.__dict__
	def load(self, obj):
		self.__dict__.clear()
		self.__dict__.update(obj)

class Intro(Quest):
	def __init__(self):
		Quest.__init__(self)
		self.t = 0
		self.progress = 0
	def think(self, dt):
		if self.done:
			return
		self.t += dt
		if self.progress == 0 and self.t > 1:
			self.progress += 1
			self.t = 0
			
		if self.progress == 1:
			hud.show("Use arrow keys or WASD to move.")


def think(dt):
	for quest in quests.values():
		quest.think(dt)

Intro()

