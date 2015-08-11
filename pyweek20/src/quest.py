from src import state, hud, thing, dialog, window

quests = {}

# Quest data members need to be JSONable

class Quest(object):
	def __init__(self):
		quests[self.__class__.__name__] = self
		self.done = False
		self.available = False
		self.t = 0
		self.progress = 0
	def dump(self):
		return self.__dict__
	def load(self, obj):
		self.__dict__.clear()
		self.__dict__.update(obj)

class Intro(Quest):
	def __init__(self):
		Quest.__init__(self)
	def think(self, dt):
		if self.done or not self.available:
			return
		self.t += dt
		if self.progress < 3 and self.t > 1:
			hud.show("Use arrow keys or WASD to move.")
			if window.distance(state.you, state.target) < 1:
				self.progress += 1
				if self.progress == 3:
					self.t = 0
					# choose target ship
				else:
					pass
					# choose new target
		

class FirstSatellite(Quest):
	def __init__(self):
		Quest.__init__(self)
	def think(self, dt):
		if self.done or not self.available:
			return
		self.t += dt
		if self.progress == 0 and self.t > 1:
			dialog.play("firstsatellite1")
			self.progress = 1
			payload = thing.Payload(pos = state.worlddata["payloads"][0])
			state.objs.append(payload)
			state.goals.append(payload)
			self.goal = payload.thingid
		if self.progress == 1:
			payload = thing.get(self.goal)
			if window.distance(payload, state.you) < 5:
				dialog.play("firstsatellite2")
				self.progress = 2
		if self.progress == 2:
			if state.you.y >= state.R - 10:
				dialog.play("firstsatellite3")
				self.progress = 3
			

def think(dt):
	for quest in quests.values():
		quest.think(dt)

Intro()
FirstSatellite()

def dump():
	data = {}
	for qname, quest in quests.items():
		data[qname] = quest.dump()
	return data
def load(obj):
	for qname, quest in quests.items():
		quest.load(data[qname])

