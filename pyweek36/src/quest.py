import math
from . import enco, thing, state, ptext, pview, progress, settings, sound
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
	def controlinfo(self):
		return []
	def marquee(self, text):
		marquee.append(text)
	def numspot(self):
		return sum(spot.unlocked for spot in state.spots)
	def drawtitle(self):
		return False

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
			t = max(self.t, self.queue[-1][0] + 1)
		self.queue.append((t, text))
	def draw(self):
		for t, text in self.queue:
			f = self.f(t)
			if not 0 < f < 1:
				continue
			alpha = math.dsmoothfade(f, 0, 1, 0.2)
			y = math.mix(600, 500, f)
			ptext.draw(text.upper(), center = T(640, y), fontsize = T(30),
				color = "#221100", ocolor = "white", owidth = 0.3,
				shade = 1, alpha = alpha)

marquee = Marquee()


@Quest()
class ArriveQuest:
	nstep = 10
	def drawtitle(self):
		return self.jstep <= 1
	def info(self):
		if self.jstep == 1:
			return "Fly to the station."
		if self.jstep == 2:
			return "New controls appear in the bottom left as you unlock abilities."
		if self.jstep == 3:
			if self.tstep > 30 and state.homeconvo == 1:
				return "Are you having trouble? Come back to the station for tips if you want."
			else:
				return "Hit a piece of unmatter to track it. Look at the background stars. And don't worry about getting close, it can't hurt ya."
		if self.jstep == 4:
			if self.tstep > 60 and state.homeconvo == 1:
				return "Are you having trouble? Come back to the station for tips if you want."
			elif state.xp == 1:
				return "You got one! Find and track 3 pieces of unmatter."
		if self.jstep == 5:
			return "Great job! Come back to the station."
		if self.jstep == 7 and state.xp == 3:
			return "Keep finding unmatter until the station counter reads 4."
		if self.jstep == 7 and state.xp == 5:
			return "Return to the station at any time for repairs and to purchase upgrades."
		if self.jstep == 8:
			return "The counter is down to 4! Come back to the station."
	def controlinfo(self):
		if self.jstep == 1:
			return [
				"Arrow keys or WASD: move",
				"Tab: change zoom level",
				"F9: calibrate difficulty",
				"F10: change resolution",
				"F11: toggle fullscreen",
				"Esc: quit (autosaved)",
			]
		return [
			"Space, Enter: throw gravnet",
			"Arrow keys or WASD: move",
			"Tab: change zoom level",
			"F9: calibrate difficulty",
			"F10: change resolution",
			"F11: toggle fullscreen",
			"Esc: quit (autosaved)",
		]
	def think(self, dt):
		if self.jstep == 0:
			state.homeconvo = 0
			self.advance()
		if self.jstep == 1 and state.at is state.home:
			progress.upgrade("gravnet")
			self.advance()
		if self.jstep == 2 and state.shots:
			state.homeconvo = 1
			self.advance()
		if self.jstep == 3 and state.xp >= 1:
			self.advance()
		if self.jstep == 4 and state.xp >= 3:
			state.homeconvo = 2
			self.advance()
		if self.jstep == 5 and state.at is state.home:
			progress.upgrade("count")
			state.techlevel["drag"] = 2
			self.advance()
			self.marquee("Tech unlocked: Counter")
			sound.play("unlock")
		if self.jstep == 6 and self.tstep > 1:
			state.homeconvo = 3
			self.advance()
		if self.jstep == 7 and state.home.nunfound() <= 4:
			state.homeconvo = 4
			self.advance()
		if self.jstep == 8 and state.at is state.home:
			progress.upgrade("count")
			quests[:] = [UnlockBeamQuest(), UnlockRingQuest(), UnlockGlowQuest()] + quests
			self.advance()
		if self.jstep < 6:
			state.you.pos = math.vclamp(state.you.pos, settings.countradius)

@Quest()
class UnlockBeamQuest:
	nstep = 10
	def info(self):
		if self.jstep == 2 and self.tstep < 20:
			return "Keep hunting unmatter, and watch for a piece of unmatter that's moving away from the station."
		if self.jstep == 3 and self.tstep < 20:
			return "If you find a cluster of unmatter, you must be near a gravity well. Locate 3 pieces to deploy a counter  there."
		if self.jstep == 5 and self.tstep < 10:
			return "Head back to the station. I've got something for ya."
		if self.jstep == 6:
			return "Press 1 to activate the Xazer beam."
		if self.jstep == 7 and self.tstep < 10:
			return "The beam will last until you throw a gravnet, so make it count."
		if self.jstep == 8 and self.tstep < 10:
			return "Return to the station whenever you want to refill your charge."
	def controlinfo(self):
		if state.techlevel["beam"] > -1:
			return ["1: activate Xazer Beam (uses charge)"]
	def think(self, dt):
		if self.jstep == 0 and state.at is state.home:
			self.advance()
		if self.jstep == 1 and state.at is not state.home:
			self.advance()
		if self.jstep == 2 and self.numspot() > 1:
			self.advance()
		if self.jstep == 2 and any(thing.dist(state.you, spot) < settings.countradius for spot in state.spots if spot is not state.home):
			self.advance()
		if self.jstep == 3 and self.numspot() > 1:
			state.homeconvo = "beam"
			self.advance()
		if self.jstep == 4 and (self.tstep >= 10 or state.at is state.home):
			self.advance()
		if self.jstep == 5 and state.at is state.home:
			self.marquee("Tech unlocked: Xazer beam")
			sound.play("unlock")
			progress.upgrade("energy")
			progress.upgrade("beam")
			self.advance()
		if self.jstep == 6 and state.you.beamon:
			self.advance()
			state.homeconvo = "more"
		if self.jstep == 7 and not state.you.beamon:
			self.advance()
		if self.jstep == 8 and state.at is state.home:
			self.advance()

@Quest()
class UnlockRingQuest:
	nstep = 4
	def info(self):
		if self.jstep == 2 and self.tstep < 10:
			return "Head back to the station. I've got something for ya."
	def controlinfo(self):
		if state.techlevel["ring"] > -1:
			return ["2: activate Linz flare (uses charge)"]
	def think(self, dt):
		if self.jstep == 0 and sum(spot.unlocked for spot in state.spots) > 3:
			state.homeconvo = "ring"
			self.advance()
		if self.jstep == 1 and (self.tstep >= 10 or state.at is state.home):
			self.advance()
		if self.jstep == 2 and state.at is state.home:
			self.marquee("Tech unlocked: Linz flare")
			sound.play("unlock")
			progress.upgrade("ring")
			self.advance()

@Quest()
class UnlockGlowQuest:
	nstep = 4
	def info(self):
		if self.jstep == 2 and self.tstep < 10:
			return "Head back to the station. I've got something for ya."
	def controlinfo(self):
		if state.techlevel["glow"] > -1:
			return ["3: activate Searchlight (uses charge)"]
	def think(self, dt):
		if self.jstep == 0 and sum(spot.unlocked for spot in state.spots) > 5:
			state.homeconvo = "glow"
			self.advance()
		if self.jstep == 1 and (self.tstep >= 10 or state.at is state.home):
			self.advance()
		if self.jstep == 2 and state.at is state.home:
			self.marquee("Tech unlocked: Searchlight")
			sound.play("unlock")
			progress.upgrade("glow")
			self.advance()

@Quest()
class PurchasesQuest:
	nstep = 10
	def controlinfo(self):
		lines = []
		if state.techlevel["drive"]:
			lines.append("4: activate Hyperdrive (uses charge)")
		if state.techlevel["map"]:
			lines.append("Hold 5 or M: view map")
		if state.techlevel["return"]:
			lines.append("Backspace: warp back to station")
		return lines

def init():
	quests[:] = [
		PurchasesQuest(),
		ArriveQuest(),
	]

def think(dt):
	for q in quests:
		q.think(dt)
	quests[:] = [q for q in quests if not q.done]

def info():
	infos = [q.info() for q in quests]
	return "\n".join(info for info in infos if info)

def getcontrolinfo():
	return [info for q in quests for info in (q.controlinfo() or [])]

def drawtitle():
	return any(q.drawtitle() for q in quests)
