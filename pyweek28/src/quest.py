# The module is called "quest", but really anything that involves progress can be a quest, including
# tutorials and instructions. This is basically a dumping ground for detailed progression we don't
# want to put anywhere else.

from . import dialog, state, view

# List of currently active quests
active = []

# TODO: I'm sure this could be done better. But for the most part I prefer outside modules not
# access the Quest instances directly.
def getquestinstance(questname):
	for obj in globals().values():
		try:
			if obj.name == questname:
				return obj()
		except:
			pass

def start(questname):
	q = getquestinstance(questname)
	q.done = False
	q.step = 0
	q.start()
	active.append(q)

def think(dt):
	for q in active:
		q.think(dt)
	active[:] = [q for q in active if not q.done]


class Quest:
	name = "QUEST"
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
	name = "testquest"
	def think(self, dt):
		Quest.think(self, dt)
		if self.step == 0 and self.t > 0.3:
			dialog.run("Want a quest, huh? Visit the Northeast side of Skyburg.")
			self.advance()
		if self.step == 1:
			s = state.currentstation()
			if s and s.name == "Skyburg" and view.dA(view.A, 5/8) == 0:
				dialog.run("Congratulations. You finished a quest. Want a reward? Tough, we haven't implemented it yet!")
				self.advance()
				self.done = True


