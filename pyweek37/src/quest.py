from . import state, generate

class Quest:
	nsteps = 1
	def __init__(self):
		self.t = 0
		self.step = 0
		self.done = False
		self.tstep = 0
	def think(self, dt):
		self.t += dt
		self.tstep += dt
		self.check()
	def check(self):
		pass
	def marquee(self):
		return None
	def advance(self):
		self.step += 1
		self.tstep = 0
		if self.step >= self.nsteps:
			self.done = True


class TutorialQuest(Quest):
	nsteps = 5
	def check(self):
		if self.step == 0 and state.allsupplied():
			self.advance()
			generate.tutorial2()
		if self.step == 1 and state.allsupplied():
			self.advance()
			generate.tutorial3()
		if self.step == 2 and state.allsupplied():
			self.advance()
			generate.tutorial4()
		if self.step == 3 and state.allsupplied():
			self.advance()
			generate.tutorial5()
		if self.step == 4 and state.allsupplied():
			self.advance()
	def marquee(self):
		if self.step == 0:
			return "Welcome to the Windswept Waste. Left click and drag from the western dome to the eastern dome to connect them and transfer a resource."	
		if self.step == 1:
			return "Each dome requires certain resources to activate, and provides certain resources when activated. Chain domes together in the right order to satisfy all the requirements."
		if self.step == 2:
			return "Resources can be routed through activated domes, if there's not room to go around."
		if self.step == 3:
			return "Domes may require more than one resource, and may provide more than one resource. Each tube can only transfer only one of a single type of resource."
		if self.step == 4:
			return "Good luck, and remember, trust in the tubes. Only through tubes may we survive."

quests = []
def inittutorial():
	quests.append(TutorialQuest())

def think(dt):
	global quests
	for q in quests:
		q.think(dt)
	quests = [q for q in quests if not q.done]

def marquee():
	for q in quests:
		if q.marquee():
			return q.marquee()

