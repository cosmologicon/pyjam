# The module is called "quest", but really anything that involves progress can be a quest, including
# tutorials and instructions. This is basically a dumping ground for detailed progression we don't
# want to put anywhere else.

from . import dialog, state, view

# List of currently active quests
active = []

def start(q):
	q.start()
	active.append(q)

def think(dt):
	for q in active:
		q.think(dt)
	active[:] = [q for q in active if not q.done]


class Quest:
	def start(self):
		self.done = False
		self.step = 0
		self.t = 0  # Time spent in current step
	def think(self, dt):
		self.t += dt
	def advance(self):
		self.step += 1
		self.t = 0

class TestQuest(Quest):
	def think(self, dt):
		Quest.think(self, dt)
		if self.step == 0 and self.t > 0.3:
			dialog.run("Want a quest, huh? Visit the Northeast side of Skyburg.")
			self.advance()
		if self.step == 1:
			s = state.currentstation()
			if s and s.name == "Skyburg" and view.dA(view.A, 1) == 0:
				dialog.run("Congratulations. You finished a quest. Want a reward? Tough, we haven't implemented it yet!")
				self.advance()
				self.done = True

class ReallocateQuest(Quest):
	def think(self, dt):
		Quest.think(self, dt)
		if self.step == 0 and self.t > 0.3:
			dialog.run("Quest: reassign one worker from Counterweight to each of the other four stations. All stations must have a worker at the same time to complete the quest.")
			self.advance()
		if self.step == 1:
			if all(s.held for s in state.stations):
				dialog.run("Congratulations. You finished a quest. Want a reward? Tough, we haven't implemented it yet!")
				self.advance()
				self.done = True

class MissionQuest(Quest):
	def __init__(self, station, need, reward):
		self.station = station
		self.need = need
		self.reward = reward
		self.progress = 0
		self.tdone = 0
	def fulfilled(self):
		pnames = [held.name for held in self.station.held]
		return all(pnames.count(name) >= self.need.count(name) for name in set(self.need))
	def think(self, dt):
		if self.fulfilled():
			self.tdone += dt
		if self.step == 0 and self.tdone > 0.5:
			self.advance()
			self.done = True
			self.finish()
	def finish(self):
		if self.reward is None:
			dialog.run("Completed: some quest that does literally nothing.")
		else:
			raise ValueError("Unknown reward %s" % self.reward)

