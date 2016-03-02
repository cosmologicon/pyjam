import math
from . import state, hud, control, gamedata, thing, background, sound

quests = {}
def init():
	quests["intro"] = IntroQuest()
	quests["objq"] = ObjectiveQQuest()
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

class ObjectiveQQuest(Quest):
	goal = 1
	def __init__(self):
		Quest.__init__(self)
		self.x0, self.y0 = gamedata.data["start"]
		self.towers = [
			thing.ObjectiveQTower(pos = [self.x0 + 10, self.y0, 0]),
			thing.ObjectiveQTower(pos = [self.x0 - 10, self.y0, 0]),
		]
		for tower in self.towers:
			state.state.addbuilding(tower)
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0:
			self.towers[0].addneed(0, 50)
			state.state.effects.append(thing.NeedIndicator(pos = self.towers[0].pos(), needtype = 0))
			self.advance()


class Act3Quest(Quest):
	goal = 99
	def __init__(self):
		Quest.__init__(self)
		x, y = gamedata.data["objectivex"]
		self.objective = thing.ObjectiveX(pos = [x, y, 0])
		state.state.addbuilding(self.objective)
		background.reveal(x, y, 50)
		self.towers = []
		for j in range(5):
			r, theta = 24, 1 + 2 * math.pi * j / 5
			tower = thing.ObjectiveXTower(pos = [x + r * math.sin(theta), y + r * math.cos(theta), 0])
			state.state.addbuilding(tower)
			self.towers.append(tower)
		self.lightning = None
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0:
			if len(self.objective.visitors) >= 5:
				sound.play("startact3")
				self.advance()
		elif self.progress == 1:
			if self.tstep >= 1:
				control.assemble(self.objective.x + 6, self.objective.y + 6)
				self.advance()
		elif self.progress == 2:
			if self.tstep > 5 and dialog.tquiet > 1:
				self.startpart1()
				self.advance()
		elif self.progress == 3:
			self.playpart1()
			if self.tstep > 60:
				self.advance()


	def startpart1(self):
		self.lightning = state.state.effects.append(thing.BallLightning(pos = [x, y, 5]))

	def playpart1(self):
#		state.state.effects.append(thing.NeedIndicator(pos = [x, y, 0], need = 0))
		pass


