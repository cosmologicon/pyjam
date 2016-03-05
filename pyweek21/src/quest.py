import math, random, pygame
from . import state, hud, control, gamedata, thing, background, sound, ptext, dialogue, settings
from . import window
from .util import F

quests = {}
def init():
	quests["credits"] = CreditsQuest()
	quests["controls"] = ControlsQuest()
	quests["intro"] = IntroQuest()
	quests["objp"] = ObjectivePQuest()
	quests["objq"] = ObjectiveQQuest()
	quests["objr"] = ObjectiveRQuest()
	quests["objs"] = ObjectiveSQuest()
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

class CreditsQuest(Quest):
	goal = 20
	def __init__(self):
		Quest.__init__(self)
		self.credits = [
			("Screenplay", "Charles McPillan\nChristopher Night"),
			("Music", "Mary Bichner"),
			("Character art", "Molly Zenobia"),
			("3d modeling", "Charles McPillan\nChristopher Night"),
			("Audio production", "Mary Bichner"),
			("Voices", "Randy Parcel\nMonica Vargas\nCharles McPillan\nMary Bichner"),
			("Testing", "John Pilman"),
			("a game by", "Christopher Night"),
		]
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0:
			if dialogue.tquiet > 4:
				self.advance()
		if self.progress == 1:
			if self.tstep > 4:
				self.advance()
		if self.progress in (2,4,6,8,10,12,14,16,18):
			if self.tstep > 1 and dialogue.tquiet > 4:
				self.advance()
		if self.progress in (3,5,7,9,11,13,15,17,19):
			if self.tstep > 4:
				self.advance()

	def draw(self):
		if self.done:
			return
		if self.progress in (1,3,5,7,9,11,13,15,17,19):
			alpha = min(max(self.tstep, 0), 1)
		elif self.progress in (2,4,6,8,10,12,14,16,18):
			alpha = min(max(1 - self.tstep, 0), 1)
		else:
			return
		if alpha == 0:
			return
		if self.progress in (1, 2):
			ptext.draw(settings.gamename.upper(), fontsize = F(70), fontname = "Oswald", alpha = alpha, 
				midright = F(840, 240), shadow = (1, 1))
		if 3 <= self.progress < 19:
			category, names = self.credits[(self.progress - 3) // 2]
			ptext.draw(category, fontsize = F(28), alpha = alpha, 
				color = "white", fontname = "Righteous",
				bottomright = F(840, 210), shadow = (1, 1))
			ptext.draw(names, fontsize = F(28), alpha = alpha,
				color = "yellow", fontname = "Righteous",
				topright = F(840, 210), shadow = (1, 1))

class ControlsQuest(Quest):
	goal = 10
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0 and dialogue.tquiet > 4:
			self.advance()
		if self.progress == 1:
			hud.show("Select: left-click\nGo: right-click or Enter")
			if self.tstep > 8:
				self.advance()
		if self.progress == 2 and dialogue.tquiet > 4 and self.tstep > 1:
			self.advance()
		if self.progress == 3:
			hud.show("Pan: arrows or WASD\nHold space: follow ship")
			if self.tstep > 8:
				self.advance()
		if self.progress == 4 and dialogue.tquiet > 4 and len(state.state.team) > 1:
			self.advance()
		if self.progress == 5:
			hud.show("Select multiple: Left drag\nAdd to selection: Ctrl+click or Shift+click")
			if self.tstep > 8:
				self.advance()
		if self.progress == 6:
			if self.tstep > 1:
				hud.show("Select all: double click\nCycle selection: Tab")
			if self.tstep > 9:
				self.advance()

class IntroQuest(Quest):
	goal = 5
	def __init__(self):
		Quest.__init__(self)
		x, y = gamedata.data["you"]["a"]
		you = thing.ShipA(pos = [x, y, settings.shipheight])
		background.reveal(x, y, 80)
		state.state.addtoteam(you)
		window.snapto(you)

		for x, y, needs, size in gamedata.data["b"]:
			if size == 1:
				building = thing.Building(pos = [x, y, 0])
			elif size == 10:
				building = thing.BigBuilding(pos = [x, y, 0])
			for needtype in needs:
				building.addneed(needtype, 1000)
			state.state.addbuilding(building)

		x, y = gamedata.data["you"]["b"]
		self.shipb = thing.ShipB(pos = [x, y, settings.shipheight])
		state.state.ships.append(self.shipb)
		x, y = gamedata.data["you"]["c"]
		self.shipc = thing.ShipC(pos = [x, y, settings.shipheight])
		state.state.ships.append(self.shipc)
		for x, y in gamedata.data["dec"]:
			state.state.adddecoration(thing.Decoration(pos = [x, y, 0]))
		for x, y in gamedata.data["smoke"]:
			smoke = thing.Smoke(pos = [x, y, 0])
			for _ in range(100):
				smoke.think(0.1)
			state.state.adddecoration(smoke)

	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0 and self.tstep > 1:
			dialogue.play("MEETA")
			self.advance()
		if self.progress == 1:
			if self.shipb not in state.state.team and self.shipb.revealed():
				state.state.addtoteam(self.shipb)
				background.reveal(self.shipb.x, self.shipb.y, 125)
				window.targetpos(self.shipb.x, self.shipb.y, self.shipb.z)
				dialogue.play("MEETB")
				self.advance()
		if self.progress == 2 and dialogue.tquiet > 30:
			dialogue.play("CHAT1")
			self.advance()
		if self.progress == 3:
			if self.shipc not in state.state.team and self.shipc.revealed():
				state.state.addtoteam(self.shipc)
				background.reveal(self.shipc.x, self.shipc.y, 125)
				window.targetpos(self.shipc.x, self.shipc.y, self.shipc.z)
				dialogue.play("MEETC")
				self.advance()
		if self.progress == 4 and dialogue.tquiet > 30:
			dialogue.play("CHAT2")
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
	goal = 3
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
		self.ship = thing.ShipD(pos = [x, y, settings.shipheight])
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0 and self.towers[0].allcharged:
			self.advance()
		if self.progress == 1 and self.tstep > 4:
			state.state.addtoteam(self.ship)
			window.targetpos(self.ship.x, self.ship.y, self.ship.z)
			self.advance()
			dialogue.play("MEETD")
		if self.progress == 2 and dialogue.tquiet > 100:
			dialogue.play("CHATD")
			self.advance()

class ObjectiveSQuest(Quest):
	goal = 3
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
		self.ship = thing.ShipF(pos = [x, y, settings.shipheight])
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0 and self.towers[0].allcharged:
			self.advance()
		if self.progress == 1 and self.tstep > 4:
			state.state.addtoteam(self.ship)
			window.targetpos(self.ship.x, self.ship.y, self.ship.z)
			self.advance()
			dialogue.play("MEETF")
		if self.progress == 2 and dialogue.tquiet > 20:
			dialogue.play("CHATF")
			self.advance()

class ObjectiveQQuest(Quest):
	goal = 3
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
		self.ship = thing.ShipE(pos = [x, y, settings.shipheight])
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
				dialogue.play("MEETE")
		if self.progress == 2 and dialogue.tquiet > 100:
			dialogue.play("CHATE")
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
		# WHERE'S THE BUG?!
		self.xmits = [thing.ObjectiveXTransmit(pos = [100, 100, 0]) for x, y in gamedata.data["xmit"]]
		for (x, y), xmit in zip(gamedata.data["xmit"], self.xmits):
			xmit.x = x
			xmit.y = y
		self.lightning = None
	def think(self, dt):
		Quest.think(self, dt)
		if self.progress == 0:
			if self.objective.revealed():
				background.reveal(self.objective.x, self.objective.y, 140)
				dialogue.play("X1")
				self.advance()
		elif self.progress == 1:
			if len(state.state.team) >= 5 and dialogue.tquiet > 22:
				dialogue.play("X2")
				self.advance()
		elif self.progress == 2:
			if len(self.objective.visitors) >= 5 and dialogue.tquiet > 3:
				sound.play("startact3")
				self.advance()
				background.revealall()
				state.state.final = True
				for k, v in list(quests.items()):
					if v is not self:
						del quests[k]
		elif self.progress == 3:
			if self.tstep >= 1:
				control.assemble(self.objective.x + 20, self.objective.y + 20)
				dialogue.play("X3")
				self.advance()
		elif self.progress == 4:
			if self.tstep > 5 and dialogue.tquiet > 1:
				self.startpart1()
				self.advance()
		elif self.progress == 5:
			self.playpart1(dt)
			if self.tstep > 120:
				dialogue.play("X4")
				self.advance()
				self.startpart2()
		elif self.progress == 6:
			self.playpart2()
			if all(xmit.active for xmit in self.xmits):
				self.advance()
		elif self.progress == 7:
			self.shake()
			if self.tstep > 3:
				from . import scene, endscene
				scene.swap(endscene)
				dialogue.play("X5")
				self.advance()
		elif self.progress == 8:
			self.shake()

	def draw(self):
		if self.progress == 5:
			ntower = sum(tower.ischarged() for tower in self.towers)
			ptext.draw("Charge cycle: %.1f/120" % self.tstep, fontsize = F(30),
				fontname = "Oswald",
				color = "red", owidth = 1.5, midbottom = F(854/2 - 200, 460))
			ptext.draw("Towers charged: %d/5" % ntower, fontsize = F(30),
				fontname = "Oswald",
				color = "yellow", owidth = 1.5, midbottom = F(854/2 + 200, 460))
		if self.progress == 6:
			for a, b in self.pairs:
				color = random.choice([(255, 255, 0), (200, 200, 200), (255, 127, 127)])
				thick = random.uniform(1, 4)
				dx0, dy0, dz0, dx1, dy1, dz1 = [random.gauss(0, 0.6) for _ in range(6)]
				x0, y0, z0 = a.pos()
				z0 += a.centerdz()
				x1, y1, z1 = b.pos()
				z1 += b.centerdz()
				p0 = window.worldtoscreen(x0 + dx0, y0 + dy0, z0 + dz0)
				p1 = window.worldtoscreen(x1 + dx1, y1 + dy1, z1 + dz1)
				pygame.draw.line(window.screen, color, p0, p1, F(thick))

	def startpart1(self):
		x, y = self.objective.x, self.objective.y
		self.lightning = thing.BallLightning(pos = [x, y, 26])
		state.state.effects.append(self.lightning)
		self.tneed = 0
		for tower in self.towers:
			tower.addcharge(None, 10000)

	def playpart1(self, dt):
		self.tneed += dt
		if self.tneed > 8:
			self.tneed = 0
			ns = set()
			while len(ns) < (1 if self.tstep < 20 else 2 if self.tstep < 50 else 3):
				ns.add(random.choice(range(5)))
			for n in ns:
				needtype = random.choice(range(3))
				tower = self.towers[n]
				tower.addneed(needtype, 30)
				state.state.effects.append(thing.NeedIndicator(pos = tower.pos(), needtype = needtype))
				state.state.effects.append(thing.NeedConnector(pos0 = self.lightning.pos(), pos1 = tower.pos(), needtype = needtype))
		ntower = sum(tower.ischarged() for tower in self.towers)
		if ntower < 3:
			self.restart()
			sound.play("restartx")

	def startpart2(self):
		sound.play("startx2")
		self.lightning.charged = True
		for tower in self.towers:
			tower.fullycharge()
		for xmit in self.xmits:
			state.state.addbuilding(xmit)
		self.pairs = []
		self.dx, self.dy = 0, 0

	def playpart2(self):
		ons = [self.objective] + [xmit for xmit in self.xmits if xmit.active]
		offs = state.state.team + [xmit for xmit in self.xmits if not xmit.active]
		def close(obj1, obj2):
			return (obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2 < 28 ** 2
		self.pairs = []
		while any(close(a, b) for a in ons for b in offs):
			for b in list(offs):
				closes = [a for a in ons if close(a, b)]
				if closes:
					ons.append(b)
					offs.remove(b)
					self.pairs.extend([a, b] for a in closes)
		for xmit in self.xmits:
			if not xmit.active and xmit in ons:
				xmit.active = True
				sound.play("xmiton")
		self.shake()

	def shake(self):
		ndx, ndy = random.uniform(-1.2, 1.2), random.uniform(-1.2, 1.2)
		window.x0 += ndx - self.dx
		window.y0 += ndy - self.dy
		self.dx, self.dy = ndx, ndy


	def restart(self):
		self.tstep = 0
		for tower in self.towers:
			tower.addneed(None, 1)
		control.assemble(self.objective.x + 20, self.objective.y + 20)
		self.tneed = 0
		for tower in self.towers:
			tower.fullycharge()


