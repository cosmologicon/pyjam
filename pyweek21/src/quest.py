import math, random
from . import state, hud, control, gamedata, thing, background, sound, ptext, dialogue, settings
from . import window
from .util import F

quests = {}
def init():
	quests["credits"] = CreditsQuest()
	quests["intro"] = IntroQuest()
	quests["objp"] = ObjectivePQuest()
	quests["objq"] = ObjectiveQQuest()
	quests["objr"] = ObjectiveRQuest()
	quests["objs"] = ObjectiveSQuest()
	quests["island"] = IslandQuest()
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

class IslandQuest(Quest):
	goal = 1
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0 and len(state.state.team) >= 3:
			background.reveal(750, -860, 180)
			self.advance()

class CreditsQuest(Quest):
	goal = 10
	def __init__(self):
		Quest.__init__(self)
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0:
			if dialogue.tquiet > 4:
				self.advance()
		if self.progress == 1:
			if self.tstep > 4:
				self.advance()
		if self.progress == 2:
			if self.tstep > 1 and dialogue.tquiet > 4:
				self.advance()
		if self.progress == 3:
			if self.tstep > 4:
				self.advance()

	def draw(self):
		if self.done:
			return
		if self.progress in (1,3):
			alpha = min(max(self.tstep, 0), 1)
		elif self.progress in (2,4):
			alpha = min(max(1 - self.tstep, 0), 1)
		else:
			return
		if alpha == 0:
			return
		if self.progress in (1, 2):
			ptext.draw(settings.gamename.upper(), fontsize = F(70), alpha = alpha, 
				midright = F(840, 240), shadow = (1, 1))
		if self.progress in (3, 4):
			ptext.draw("by Christopher Night", fontsize = F(48), alpha = alpha, 
				color = "yellow",
				midright = F(840, 240), shadow = (1, 1))


class IntroQuest(Quest):
	goal = 2
	def __init__(self):
		Quest.__init__(self)
		x, y = gamedata.data["you"]["b"]
		self.shipb = thing.ShipB(pos = [x, y, 4])
		state.state.ships.append(self.shipb)
		x, y = gamedata.data["you"]["c"]
		self.shipc = thing.ShipC(pos = [x, y, 4])
		state.state.ships.append(self.shipc)
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0:
			if self.shipb not in state.state.team and self.shipb.revealed():
				state.state.addtoteam(self.shipb)
				background.reveal(self.shipb.x, self.shipb.y, 125)
				# dialogue.play("meetb")
				self.advance()
		if self.progress == 1:
			if self.shipc not in state.state.team and self.shipc.revealed():
				state.state.addtoteam(self.shipc)
				background.reveal(self.shipc.x, self.shipc.y, 125)
				# dialogue.play("meetc")
				self.advance()
		

class ObjectivePQuest(Quest):
	goal = 1
	def __init__(self):
		Quest.__init__(self)
		self.towers = [
			thing.ObjectivePTower(pos = [x, y, 0], needtype = j)
			for j, (x, y) in enumerate(gamedata.data["p"])
		]
		for j, tower in enumerate(self.towers):
			state.state.addbuilding(tower)
			tower.addtowers(self.towers)
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0 and self.towers[0].allcharged:
			self.advance()

class ObjectiveRQuest(Quest):
	goal = 2
	def __init__(self):
		Quest.__init__(self)
		self.towers = [
			thing.ObjectivePTower(pos = [x, y, 0], needtype = j)
			for j, (x, y) in enumerate(gamedata.data["r"])
		]
		for j, tower in enumerate(self.towers):
			state.state.addbuilding(tower)
			tower.addtowers(self.towers)
		x, y = gamedata.data["you"]["d"]
		self.ship = thing.ShipD(pos = [x, y, 4])
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0 and self.towers[0].allcharged:
			self.advance()
		if self.progress == 1 and self.tstep > 4:
			state.state.addtoteam(self.ship)
			window.targetpos(self.ship.x, self.ship.y, self.ship.z)
			self.advance()

class ObjectiveSQuest(Quest):
	goal = 2
	def __init__(self):
		Quest.__init__(self)
		self.towers = [
			thing.ObjectivePTower(pos = [x, y, 0], needtype = j)
			for j, (x, y) in enumerate(gamedata.data["s"])
		]
		for j, tower in enumerate(self.towers):
			state.state.addbuilding(tower)
			tower.addtowers(self.towers)
			tower.imgname = "objs"
			tower.scale = 20
		x, y = gamedata.data["you"]["f"]
		self.ship = thing.ShipF(pos = [x, y, 4])
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0 and self.towers[0].allcharged:
			self.advance()
		if self.progress == 1 and self.tstep > 4:
			state.state.addtoteam(self.ship)
			window.targetpos(self.ship.x, self.ship.y, self.ship.z)
			self.advance()

class ObjectiveQQuest(Quest):
	goal = 2
	def __init__(self):
		Quest.__init__(self)
		self.towers = [
			thing.ObjectiveQTower(pos = [x, y, 0], needtype = None)
			for j, (x, y) in enumerate(gamedata.data["q"])
		]
		for tower in self.towers:
			state.state.addbuilding(tower)
			tower.addtowers(self.towers)
			for needtype in (0, 1, 2):
				tower.addneed(needtype, 1000)
		self.towers[1].imgname = "objq1"
		x, y = gamedata.data["you"]["e"]
		self.ship = thing.ShipE(pos = [x, y, 4])
		self.tneed = 0
		self.jneed = 0
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0:
			if self.towers[0].allcharged:
				self.advance()
			elif any(tower.visitors for tower in self.towers):
				self.tneed += dt
				if self.tneed > 6:
					self.tneed = 0
					needtype = random.choice((0, 1, 2))
					jtower = random.choice((0, 1))
					needtype = self.jneed % 3
					jtower = self.jneed % 2
					self.towers[jtower].addneed(needtype, 50)
					state.state.effects.append(thing.NeedIndicator(pos = self.towers[jtower].pos(), needtype = needtype))
					self.jneed += 1
		elif self.progress == 1:
			if self.tstep > 4:
				state.state.addtoteam(self.ship)
				window.targetpos(self.ship.x, self.ship.y, self.ship.z)
				self.advance()


class Act3Quest(Quest):
	goal = 99
	def __init__(self):
		Quest.__init__(self)
		x, y = gamedata.data["x"]
		self.objective = thing.ObjectiveX(pos = [x, y, 0])
		state.state.addbuilding(self.objective)
		self.towers = []
		for j in range(5):
			r, theta = 60, 2 * math.pi * j / 5
			tower = thing.ObjectiveXTower(pos = [x + r * math.cos(theta), y + r * math.sin(theta), 0])
			tower.rot = j
			tower.addneed(None, 1)
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
				control.assemble(self.objective.x + 20, self.objective.y + 20)
				self.advance()
		elif self.progress == 2:
			if self.tstep > 5 and dialogue.tquiet > 1:
				self.startpart1()
				self.advance()
		elif self.progress == 3:
			self.playpart1(dt)
			if self.tstep > 120:
				self.advance()
				self.startpart2()
		elif self.progress == 4:
			self.playpart2()

	def draw(self):
		if self.progress == 3:
			ntower = sum(tower.ischarged() for tower in self.towers)
			ptext.draw("Charge cycle: %.1f/120" % self.tstep, fontsize = F(30),
				color = "red", owidth = 1.5, midbottom = F(854 - 200, 460))
			ptext.draw("Towers charged: %d/5" % ntower, fontsize = F(30),
				color = "yellow", owidth = 1.5, midbottom = F(854 + 200, 460))

	def startpart1(self):
		x, y = self.objective.x, self.objective.y
		self.lightning = thing.BallLightning(pos = [x, y, 26])
		state.state.effects.append(self.lightning)
		self.tneed = 0
		for tower in self.towers:
			tower.addcharge(None, 10000)

	def playpart1(self, dt):
		self.tneed += dt
		if self.tneed > 12:
			self.tneed = 0
			n = random.choice(range(5))
			needtype = random.choice(range(3))
			tower = self.towers[n]
			tower.addneed(needtype, 1)
			state.state.effects.append(thing.NeedIndicator(pos = tower.pos(), needtype = needtype))
			state.state.effects.append(thing.NeedConnector(pos0 = self.lightning.pos(), pos1 = tower.pos(), needtype = needtype))
		ntower = sum(tower.ischarged() for tower in self.towers)
		if ntower < 3:
			self.restart()
			sound.play("restartx")

	def startpart2(self):
		sound.play("startx2")
		for tower in self.towers:
			tower.fullycharge()

	def playpart2(self):
		pass

	def restart(self):
		for tower in self.towers:
			tower.addneed(None, 1)
		if self.lightning is not None:
			state.state.effects.remove(self.lightning)
			self.lightning = None
		control.assemble(self.objective.x + 20, self.objective.y + 20)


