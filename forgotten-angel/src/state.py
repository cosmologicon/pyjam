import pygame, random, math, os.path
try:
	import cPickle as pickle
except ImportError:
	import pickle
from . import settings, ships, things, quest, parts, starmap, sound, bosses, scene, buildscene, dialog
from .settings import F

starmap.init()

class State(object):
	def __init__(self):
		self.bank = 0
		self.you = ships.You(starmap.ps["start"])
		if settings.quickstart:
			self.you.vmax *= 6
			self.you.a *= 6
			self.you.laser.damage *= 1000
			self.bank += 1000
		self.mother = ships.Mothership(starmap.ps["mother"])
		self.baron = ships.Baron((0, 0))
		self.supply = ships.Supply((0, 0))
		self.boss = None
		self.bossmode = False
		# points of interest
		self.interests = set()
		self.ships = [
			self.you,
			self.mother,
		]
		self.things = []
		for tname, p in starmap.ps.items():
			if tname.startswith("angel"):
				t = things.Sun(p)
				setattr(self, tname, t)
				if tname != "angel5":
					if tname == "angel4":
						t.collapsed = True
					self.things.append(t)
				else:
					t.showsup = False
			if tname.startswith("planet"):
				self.things.append(things.Planet(p))
#		for _ in range(4):
#			self.ships.append(ships.Guard(self.things[0]))
		self.effects = []
		self.quests = [
		]

		# SHIP LAYOUT
		self.parts = [
		]
		# iedges for active power supplies
		self.supplies = {
			1: (-1, 3, 0, 3),
		}
		self.parts = [
			parts.Conduit((2,)).rotate(3).shift((3, 1)),
			parts.Module("engine").shift((0, 3)),
			parts.Module("drill").shift((1, 1)),
		]
		self.available = ["engine", "drill", "laser", "scope"]
		self.unlocked = ["engine", "drill"]
		self.unused = { modulename: 0 for modulename in settings.modulecosts }
		self.unused["conduit-1"] = 2
		self.unused["conduit-2"] = 2
		self.unused["conduit-3"] = 2
		self.unused["conduit-12"] = 1
		# self.modules is a list of placed module names
		# self.powered maps module names to powered-up state
		# self.hookup maps hooked up module name to the supply numbers that feed it.
		self.sethookup()
		self.burnfactor = 0
		self.oortfactor = 0
		self.tburn = 0
		self.toort = 0
		self.tfuel = 0
		
		# dialogue
		self.played = set()
		self.playing = []
		self.tline = 0
		
		self.starssurveyed = 0

	def startnextact(self):
		act = len(self.supplies)
		if act == 1:
			self.supplies[2] = (4, 1, 3, 1)
			self.available.append("turbo")
			self.available.append("heatshield")
			self.available.append("deflector")
			self.quests.append(quest.Act2Quest())
			dialog.playfirst("act2")
			self.interests.remove("supply")
		elif act == 2:
			self.available.append("hyperdrive")
			self.supplies[3] = (-1, 1, 0, 1)
			for c in "012346789":
				self.interests.add("angel" + c)
			self.things.append(self.angel5)
			self.quests.append(quest.Act3Quest())
			dialog.playfirst("act3")
			self.interests.remove("supply")
		self.boss = None
		self.you.x, self.you.y = self.mother.x, self.mother.y
		scene.push(buildscene)


	def handlebutton(self, buttonname):
		if buttonname in self.modules:
			self.toggleactive(buttonname)
			return True

	def toggleactive(self, modulename):
		if modulename in self.hookup:
			self.active[modulename] = not self.active[modulename]
			for omname in self.hookup:
				if omname != modulename and set(self.hookup[modulename]) & set(self.hookup[omname]):
					self.active[omname] = False

	def cango(self):
		return "engine" in self.hookup or "turbo" in self.hookup or "hyperdrive" in self.hookup

	def think(self, dt):
		from . import vista
		self.bossmode = self.boss is not None and self.boss.distfromyou() < settings.fadedistance
		if self.bossmode and not self.boss.corpse.alive:
			self.startnextact()
		if not self.bossmode:
			if random.random() * 1 < dt:
				theta = random.uniform(0, math.tau)
				x = vista.x0 + settings.fadedistance * math.sin(theta)
				y = vista.y0 + settings.fadedistance * math.cos(theta)
				self.ships.append(ships.Rock((x, y)))
			if random.random() * 1 < dt:
				theta = random.uniform(0, math.tau)
				x = vista.x0 + settings.fadedistance * math.sin(theta)
				y = vista.y0 + settings.fadedistance * math.cos(theta)
				self.ships.append(ships.Drone((x, y)))
		if self.active["hyperdrive"]:
			if self.you.target:
				self.tfuel += dt
				if self.tfuel > 2:
					self.tfuel -= 2
					self.bank = max(self.bank - 1, 0)
			self.you.vmax = 20
			self.you.a = 10
		elif self.active["turbo"]:
			self.you.vmax = 8
			self.you.a = 4
		elif self.active["engine"]:
			self.you.vmax = 4
			self.you.a = 2
		else:
			self.you.allstop()
		if self.active["drill"] and self.you.drill.canfire():
			for s in self.ships:
				if s.drillable and self.you.drill.canreach(s):
					self.you.drill.fire(s)
					if s.hp <= 0:
						self.bank += s.value
						sound.play("getmoney")
		if self.active["laser"] and self.you.laser.canfire():
			for s in self.ships:
				if s.laserable and self.you.laser.canreach(s):
					self.you.laser.fire(s)
					if s.hp <= 0:
						self.bank += s.value
						sound.play("getmoney")
		if self.active["gun"] and self.you.gun.canfire():
			for s in self.ships:
				if s.laserable and self.you.gun.canreach(s):
					self.you.gun.fire(s)
					if s.hp <= 0:
						self.bank += s.worth
						sound.play("getmoney")
		for s in self.ships:
			if s.shootsyou:
				for w in s.weapons:
					if w.canfire() and w.canreach(self.you):
						w.fire(self.you)
		for t in self.things:
			t.think(dt)
		for s in self.ships:
			s.think(dt)
		for e in self.effects:
			e.think(dt)
		for q in self.quests:
			q.think(dt)
		self.ships = [s for s in self.ships if not s.faded()]
		
		self.alerts = []
		dburn = min(
			math.sqrt((self.you.x - thing.x) ** 2 + (self.you.y - thing.y) ** 2) - thing.radius
			for thing in self.things if thing.burns
		)
		if dburn < -1:
			if self.active["heatshield"]:
				self.alerts.append("Heat shield holding.")
			else:
				self.alerts.append("Danger. Hull overheating. Breach imminent.")
				self.tburn += dt
				if self.tburn > settings.burndamagetime:
					self.you.takedamage(1)
					self.tburn = 0
		elif dburn < 0:
			self.tburn = 0
			if self.active["heatshield"]:
				self.alerts.append("Heat shield holding.")
			else:
				self.alerts.append("Heat at dangerous levels. Move to a safe distance.")
		else:			
			self.tburn = 0
		a = starmap.getoort((self.you.x, self.you.y))
		if a < 0.2:
			pass
		elif a < 0.9:
			if self.active["deflector"]:
				self.alerts.append("Deflector holding.")
			else:
				self.alerts.append("Approaching the Oort. Danger of hull damage ahead.")
		else:
			if self.active["deflector"]:
				self.alerts.append("Deflector holding.")
			else:
				self.alerts.append("Danger. Hull taking damage. Breach imminent.")
				self.toort += dt
				if self.toort > settings.oortdamagetime:
					self.you.takedamage(1)
					self.toort = 0
		if self.active["scope"]:
			for t in self.things:
				if t.nearyou():
					if t.surveyed:
						self.alerts.append("Survey complete.")
					else:
						t.tsurvey += dt
						self.alerts.append("Survey in progress... %d%%" % int(t.tsurvey * 10))
						if t.tsurvey > 10:
							t.surveyed = True
							if isinstance(t, things.Sun):
								self.starssurveyed += 1
							sound.play("getmoney")
							self.bank += t.value

	def drawviewport(self):
		from . import vista, img
		a = starmap.getoort((self.you.x, self.you.y))
		vista.screen.fill((0, int(80 * a), int(60 * a)))
		vista.drawstars()
		for t in self.things:
			t.draw()
		for s in self.ships:
			s.draw()
		for e in self.effects:
			e.draw()
		for iname in self.interests:
			obj = getattr(self, iname)
			if not vista.isvisible((obj.x, obj.y), obj.radius - 1):
				pos, angle = vista.indpos((obj.x, obj.y))
				img.worlddraw("arrow", pos, angle = angle)
				img.drawtext(settings.inames[iname], F(20), (0, 255, 255), fontname = "teko", center = vista.worldtoscreen(pos))

	def drawmainmap(self):
		from . import vista, img
		vista.drawmainoort()
		scale = settings.grect.width / (2 * starmap.rx)
		for t in self.things:
			if t.surveyed:
				px, py = vista.worldtomainmap((t.x, t.y))
				r = int(scale * t.radius)
				pygame.draw.circle(vista.screen, (200, 200, 200), (px, py), r)
		for iname in self.interests:
			obj = getattr(self, iname)
			if isinstance(obj, things.Sun):
				pass
			px, py = vista.worldtomainmap((obj.x, obj.y))
#			pygame.draw.circle(vista.screen, (200, 200, 200), (px, py), F(10), 1)
			img.drawtext(settings.inames[iname], F(12), fontname = "teko", center = (px, py))
		px, py = vista.worldtomainmap((self.you.x, self.you.y))
		img.drawtext("YOU", F(12), fontname = "teko", color = (255, 200, 0), center = (px, py))
		img.drawtext("Surveyed planets and stars", F(24), fontname = "viga", center = F(240, 20))


	def drawnavmap(self):
		from . import vista, img
		vista.drawnavoort()
		for t in self.things:
			if not t.showsup:
				continue
			p = vista.worldtonav((t.x, t.y))
			r = t.radius * settings.nscale
			color = (200, 200, 200) if t.surveyed else (50, 50, 50)
			pygame.draw.circle(vista.navmap, color, p, r)
		pygame.draw.rect(vista.navmap, (128, 128, 128), vista.navmap.get_rect(), 2)
		vista.screen.blit(vista.navmap, settings.nrect)


	def unlock(self, modulename):
		if modulename not in self.available or modulename in self.unlocked:
			return
		cost = settings.modulecosts[modulename]
		if self.bank < cost:
			sound.play("cantbuy")
			return
		self.unlocked.append(modulename)
		self.unused[modulename] = 1
		self.bank -= cost
		sound.play("buy")

	def buy(self, cname):
		cost = settings.modulecosts[cname]
		if self.bank < cost:
			sound.play("cantbuy")
			return
		self.unused[cname] += 1
		self.bank -= cost
		sound.play("buy")

	def canaddpart(self, part):
		takenblocks = set(b for p in self.parts for b in p.blocks)
		return set(part.blocks).isdisjoint(takenblocks)

	def addpart(self, part):
		self.parts.append(part)
		self.sethookup()
		self.unused[part.name] -= 1

	def sethookup(self):
		powered = {
			edge: [supply] for supply, edge in self.supplies.items()
		}
		self.hookup = {}
		self.modules = [part.name for part in self.parts if part.ismodule]
		self.active = { mname: False for mname in settings.modulecosts }
		while True:
			n = len(powered)
			for part in self.parts:
				if all(edge in powered for edge in part.inputs):
					supplies = sorted(set.union(*(set(powered[edge]) for edge in part.inputs)))
					for oedge in part.outputs:
						powered[oedge] = supplies
					if part.ismodule:
						self.hookup[part.name] = supplies
			if len(powered) == n:
				break

	def partat(self, block):
		for part in self.parts:
			if tuple(block) in part.blocks:
				return part
		return None

	def removepart(self, part):
		self.parts.remove(part)
		self.sethookup()
		self.unused[part.name] += 1

	def removeall(self):
		for part in list(self.parts):
			self.removepart(part)


def save():
	pickle.dump(state, open("savegame.pkl", "wb"), 2)

def load():
	global state
	state = pickle.load(open("savegame.pkl", "rb"))

def canload():
	return os.path.exists("savegame.pkl")

def reset():
	global state
	state = State()
	state.quests.append(quest.IntroQuest())

reset()

if canload():
	load()

