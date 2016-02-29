from . import state, hud, control

quests = {}
def init():
	quests["intro"] = IntroQuest()
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

