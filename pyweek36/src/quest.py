from . import enco, thing, state

quests = []

class Quest(enco.Component):
	nstep = None
	def __init__(self):
		self.jstep = 0
		self.done = False
		self.t = 0
	def think(self, dt):
		self.t += dt
	def advance(self):
		self.jstep += 1
		if self.nstep is not None and self.jstep >= self.nstep:
			self.complete()
	def complete(self):
		self.done = True
	def info(self):
		return None

@Quest()
class ArriveQuest:
	nstep = 1
	def info(self):
		if self.jstep == 0:
			return "Arrow keys or WASD: fly to the base."
	def think(self, dt):
		if self.jstep == 0 and thing.overlaps(state.you, state.home):
			self.advance()

def init():
	quests[:] = [
		ArriveQuest(),
	]

def think(dt):
	for q in quests:
		q.think(dt)
	quests[:] = [q for q in quests if not q.done]

def info():
	infos = [q.info() for q in quests]
	return "\n".join(info for info in infos if info)

