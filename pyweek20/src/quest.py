from __future__ import division
import random
from src import state, hud, thing, dialog, window, scene, sound

quests = {}

# Quest data members need to be JSONable

class Quest(object):
	def __init__(self):
		quests[self.__class__.__name__] = self
		self.done = False
		self.available = False
		self.t = 0
		self.progress = 0
	def dump(self):
		return self.__dict__
	def load(self, obj):
		self.__dict__.clear()
		self.__dict__.update(obj)

class Intro(Quest):
	def __init__(self):
		Quest.__init__(self)
		self.tps = [
			(None, None),
			(10, 10),
			(-12, -3),
			(3, 12),
			(None, None),
			(0, 0),
			(12, 3),
			(None, None),
			(3, -12),
			(None, None),
		]
	def think(self, dt):
		if self.done or not self.available:
			return
		self.t += dt
		if self.progress == 0 and self.t > 1:
			self.progress += 1
			self.settarget()
			state.effects.append(state.target)
		if self.progress in (1, 2, 3, 5, 6, 8):
			if window.distance(state.you, state.target) < 1:
				hud.hide("Hold space (or enter, shift, or Z) and use arrows to teleport.")
				state.target.die()
				self.progress += 1
				self.settarget()
		elif self.progress in (4, 7, 9):
			if state.target is state.you:
				self.progress += 1
				self.settarget()
		if self.progress == 10:
			if not dialog.queue and not dialog.currentline:
				from src.scenes import title
				scene.current = title
				scene.toinit = title
				self.done = True
	def settarget(self):
		if self.progress > 1:
			sound.play("yes")
	
		if self.progress == 1:
			hud.show("Use arrow keys or WASD to move.")
			dialog.play("intro1")
		elif self.progress == 2:
			hud.clear()
		elif self.progress == 4:
			hud.show("Hold space (or enter, shift, or Z) and use arrows to teleport.")
			dialog.play("intro2")
		elif self.progress == 5:
			hud.clear()
		elif self.progress == 6:
			dialog.play("intro3")
		elif self.progress == 10:
			dialog.play("intro4")

		if self.progress in (1, 2, 3, 5, 6, 8):
			dx, dy = self.tps[self.progress]
			state.target = thing.Target(X = dx / window.camera.y0, y = window.camera.y0 - dy)
			state.effects.append(state.target)
		elif self.progress in (4, 7, 9):
			state.target = None
			while state.target in (None, state.you):
				state.target = random.choice(state.ships)
			state.effects.append(thing.ShipTarget(parentid = state.target.thingid))

class Act1(Quest):
	def __init__(self):
		Quest.__init__(self)
		self.goals = []
	def think(self, dt):
		if self.done or not self.available:
			return
		# TODO: play distress call (convo6)
		self.t += dt
		if self.progress == 0 and self.t > 1:
			dialog.play("convo2")
			self.progress = 1
			payloads = [
				thing.Payload(pos = pos) for pos in state.worlddata["payloads"][:3]
			]
			state.objs.extend(payloads)
			state.goals.extend(payloads)
			self.goals = [p.thingid for p in payloads]
		if self.progress == 1:
			if any(window.distance(thing.get(goal), state.you) < 20 for goal in self.goals):
				dialog.play("convo3")
				self.progress = 2
		if self.progress >= 2:
			nvisible = sum(thing.get(goal).isvisible() for goal in self.goals)
			if self.progress == 2 and nvisible >= 1:
				dialog.play("convo4")
				self.progress = 3
			if self.progress == 3 and nvisible >= 2:
				dialog.play("convo7")
				self.progress = 4
			if self.progress == 4 and nvisible == 3:
				dialog.play("convo8")
				self.progress = 5
				self.done = True
				quests["Act2"].setup()
				# TODO: stop playing distress call


class Act2(Quest):
	def __init__(self):
		Quest.__init__(self)
	def setup(self):
		self.available = True
		self.cutscened = False
		self.tquiet = 0
		payload = thing.BatesShip(pos = state.worlddata["payloads"][3])
		state.objs.append(payload)
		state.goals.append(payload)
		self.goal = payload.thingid
		state.shipyard = {
			"Skiff": 500,
			"Mapper": 500,
			"Beacon": 500,
			"Heavy": 500,
		}
		hud.show("Armored Ship unlocked", 4)
	def think(self, dt):
		if self.done or not self.available:
			return
		self.t += dt
		if not self.cutscened:
			if dialog.queue or dialog.currentline:
				self.tquiet = 0
			else:
				self.tquiet += dt
			if self.tquiet > 5:
				self.cutscened = True
				from src.scenes import act2cutscene
				from src import scene
				scene.current = act2cutscene
				scene.toinit = act2cutscene
		if self.progress == 0 and thing.get(self.goal).isvisible():
			dialog.play("convo10")
			self.progress = 1

		if self.progress == 1 and self.cutscened:
			self.done = True
			quests["Seek"].setup()


class Seek(Quest):
	def setup(self):
		self.available = True
		state.convergences = [
			thing.Convergence(X = X, y = y)
			for X, y in state.worlddata["convergences"]
		]
	def think(self, dt):
		if self.done or not self.available:
			return
		self.t += dt
		nvis = sum(convergence.isvisible() for convergence in state.convergences)
		if nvis > self.progress:
			self.updateprogress(nvis)
	def updateprogress(self, nprogress):
		self.progress = nprogress
		if nprogress == 1:
			state.shipyard = {
				"Mapper": 600,
				"BeaconSkiff": 800,
				"Heavy": 600,
			}
			hud.show("Cutter-Detector unlocked", 5)
		if nprogress == 2:
			state.shipyard = {
				"Mapper": 600,
				"BeaconSkiff": 800,
				"Heavy": 600,
				"Warp": 600,
			}
			hud.show("Warp ship unlocked", 5)
		elif nprogress == 3:
			state.shipyard = {
				"HeavyMapper": 800,
				"BeaconSkiff": 800,
				"Warp": 600,
			}
			hud.show("Armored Survey ship unlocked", 5)
		elif nprogress == 4:
			state.shipyard = {
				"HeavyMapper": 600,
				"BeaconSkiff": 600,
				"HeavySkiff": 600,
				"WarpSkiff": 600,
			}
			hud.show("Warp Cutter unlocked", 5)
		elif nprogress == 5:
			state.shipyard = {
				"HeavyMapper": 600,
				"HeavyBeacon": 600,
				"BeaconSkiff": 600,
				"HeavySkiff": 600,
				"WarpSkiff": 600,
			}
			hud.show("Armored Detector unlocked", 5)
		elif nprogress == 6:
			state.shipyard = {
				"HeavyMapper": 600,
				"HeavyBeacon": 600,
				"BeaconSkiff": 600,
				"HeavyWarpSkiff": 600,
			}
			hud.show("Armored Warp Cutter unlocked", 5)
		elif nprogress == 7:
			state.shipyard = {
				"HeavyMapper": 600,
				"HeavyBeaconSkiff": 600,
				"HeavyWarpSkiff": 600,
			}
			hud.show("Armored Cutter-Detector unlocked", 5)
		elif nprogress == 8:
			state.shipyard = {
				"HeavyMapperSkiff": 600,
				"HeavyBeaconSkiff": 600,
				"HeavyWarpSkiff": 600,
			}
			hud.show("Armored Survey Cutter unlocked", 5)


def think(dt):
	for quest in quests.values():
		quest.think(dt)

Intro()
Act1()
Act2()
Seek()

def dump():
	data = {}
	for qname, quest in quests.items():
		data[qname] = quest.dump()
	return data
def load(obj):
	for qname, quest in quests.items():
		quest.load(obj[qname])

