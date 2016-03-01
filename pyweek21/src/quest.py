import math
from . import state, hud, control, gamedata, thing, background

quests = {}
def init():
	quests["intro"] = IntroQuest()
	quests["act3"] = Act3Quest()
def think(dt):
	for qname, quest in sorted(quests.items()):
		quest.think(dt)
		if quest.done:
			del quests[qname]


class Quest(object):
	goal = 1
	def __init__(self):
		self.t = 0
		self.tstep = 0
		self.progress = 0
		self.done = False
	def advance(self):
		self.tstep = 0
		self.progress += 1
		if self.progress >= self.goal:
			self.done = True
	def think(self, dt):
		self.t += dt
		self.tstep += dt

class IntroQuest(Quest):
	goal = 1
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0:
			if self.tstep > 3:
				hud.show("Select your ship")
			if control.isselected(state.state.team[0]):
				self.advance()

class Act3Quest(Quest):
	goal = 99
	def __init__(self):
		Quest.__init__(self)
		x, y = gamedata.data["objectivex"]
		self.objective = thing.ObjectiveX(pos = [x, y, 0])
		state.state.addbuilding(self.objective)
		background.reveal(x, y, 50)
		for j in range(5):
			r, theta = 32, 1 + 2 * math.pi * j / 5
			building = thing.ObjectiveXTower(pos = [x + r * math.sin(theta), y + r * math.cos(theta), 0])
			state.state.addbuilding(building)
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0:
			len(self.objective.visitors)


