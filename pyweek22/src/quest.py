from . import dialog

def init():
	global quests
	quests = [
		IntroQuest(),
	]

def think(dt):
	for quest in quests:
		if quest.done:
			continue
		quest.think(dt)

class Quest(object):
	def __init__(self):
		self.t = 0
		self.tstep = 0
		self.jstep = 0
		self.done = False
	def think(self, dt):
		self.t += dt
		self.tstep += dt
	def advance(self):
		self.jstep += 1
		self.tstep = 0

class IntroQuest(Quest):
	def think(self, dt):
		Quest.think(self, dt)
		if self.jstep == 0:
			if dialog.tquiet > 3:
				dialog.play("intro0")
				self.advance()


