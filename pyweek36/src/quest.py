from . import enco, thing, state

quests = []
marquee = []

class Quest(enco.Component):
	nstep = None
	def __init__(self):
		self.jstep = 0
		self.done = False
		self.t = 0
		self.tstep = 0
	def think(self, dt):
		self.t += dt
		self.tstep += dt
	def advance(self):
		self.jstep += 1
		if self.nstep is not None and self.jstep >= self.nstep:
			self.complete()
		self.tstep = 0
	def complete(self):
		self.done = True
	def info(self):
		return None
	def marquee(self, text):
		marquee.append(text)

@Quest()
class ArriveQuest:
	nstep = 5
	def info(self):
		if self.jstep == 0:
			return "Arrow keys or WASD: fly to the station."
		if self.jstep == 1:
			return "Space, Enter, or left mouse click: throw a gravnet."
		if self.jstep == 2:
			if self.tstep > 30:
				return "See README.md for instructions to adjust the difficulty, if desired."
			else:
				return "Hit a piece of dark matter to track it. Look closely at the stars."
		if self.jstep == 3:
			if self.tstep > 60:
				return "See README.md for instructions to adjust the difficulty, if desired."
			else:
				return "Find and track 3 pieces of dark matter. Don't go too far."
		if self.jstep == 4:
			return "Return to the station."
	def think(self, dt):
		if self.jstep == 0 and state.at is state.home:
			state.upgrade("gravnet")
			self.advance()
		if self.jstep == 1 and state.shots:
			self.advance()
		if self.jstep == 2 and state.xp >= 1:
			self.advance()
		if self.jstep == 3 and state.xp >= 3:
			self.advance()
		if self.jstep == 4 and state.at is state.home:
			state.upgrade("engine")
			state.upgrade("gravnet")
			state.techlevel["drag"] = 2
			self.advance()
			self.marquee("Level up!")
			self.marquee("Tech unlocked: Counter")

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

def popmarquee():
	if marquee:
		ret = marquee[0]
		del marquee[0]
		return ret
	return None

