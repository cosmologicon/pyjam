import math
from . import enco, thing, state, ptext, pview, progress
from .pview import T

quests = []

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

class Marquee:
	def __init__(self):
		self.queue = []
		self.t = 0
	def f(self, t):
		return math.clamp(0.5 * (self.t - t), 0, 1)
	def think(self, dt):
		self.t += dt
		self.queue = [(t, text) for t, text in self.queue if self.f(t) < 1]
	def append(self, text):
		if not self.queue:
			t = self.t
		else:
			t = max(self.t, self.queue[-1][1] + 1)
		self.queue.append((t, text))
	def draw(self):
		for t, text in self.queue:
			f = self.f(t)
			if not 0 < f < 1:
				continue
			alpha = math.dsmoothfade(f, 0, 1, 0.2)
			y = math.mix(600, 500, f)
			ptext.draw(text, center = T(640, y), fontsize = T(60),
				color = "#442200", ocolor = "white", owidth = 0.5,
				shade = 1, alpha = alpha)

marquee = Marquee()


@Quest()
class ArriveQuest:
	nstep = 7
	def info(self):
		if self.jstep == 0:
			return "Arrow keys or WASD: fly to the station."
		if self.jstep == 1:
			return "Space, Enter, or left mouse click: throw a gravnet."
		if self.jstep == 2:
			if self.tstep > 30:
				return "See README.md for instructions to adjust the difficulty, if desired."
			else:
				return "Hit a piece of unmatter to track it. Look closely at the stars."
		if self.jstep == 3:
			if self.tstep > 60:
				return "See README.md for instructions to adjust the difficulty, if desired."
			else:
				return "Find and track 3 pieces of unmatter. Don't go too far."
		if self.jstep == 4:
			return "Return to the station."
		if self.jstep == 5 and state.xp == 3:
			return "Find more unmatter until the station counter reads 3."
		if self.jstep == 6:
			return "Return to the station."
	def think(self, dt):
		if self.jstep == 0:
			state.homeconvo = 0
		if self.jstep == 0 and state.at is state.home:
			progress.upgrade("gravnet")
			self.advance()
		if self.jstep == 1 and state.shots:
			self.advance()
		if self.jstep == 2 and state.xp >= 1:
			self.advance()
		if self.jstep == 3 and state.xp >= 3:
			state.homeconvo = 1
			self.advance()
		if self.jstep == 4 and state.at is state.home:
			progress.upgrade("engine")
			progress.upgrade("gravnet")
			progress.upgrade("count")
			state.techlevel["drag"] = 2
			self.advance()
			self.marquee("Tech unlocked: Counter")
		if self.jstep == 5:
			if state.home.nunfound() <= 3:
				state.homeconvo = 2
				self.advance()
		if self.jstep == 6 and state.at is state.home:
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



