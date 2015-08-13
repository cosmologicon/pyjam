from __future__ import division
import random
from src import state, hud, thing, dialog, window, scene

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
			dx, dy = self.tps[1]
			state.target = thing.Target(X = dx / window.camera.y0, y = window.camera.y0 + dy)
			state.effects.append(state.target)
			hud.show("Use arrow keys or WASD to move.")
		if self.progress in (1, 2, 3, 5, 6, 8):
			if window.distance(state.you, state.target) < 1:
				state.target.die()
				self.progress += 1
				self.settarget()
		elif self.progress in (4, 7, 9):
			if state.target is state.you:
				self.progress += 1
				self.settarget()
		if self.progress == 3:
			self.done = True
			from src.scenes import title
			scene.current = title
	def settarget(self):
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
	def think(self, dt):
		if self.done or not self.available:
			return
		self.t += dt
		if self.progress == 0 and self.t > 1:
			dialog.play("firstsatellite1")
			self.progress = 1
			payload = thing.Payload(pos = state.worlddata["payloads"][0])
			state.objs.append(payload)
			state.goals.append(payload)
			self.goal = payload.thingid
		if self.progress == 1:
			payload = thing.get(self.goal)
			if window.distance(payload, state.you) < 20:
				dialog.play("firstsatellite2")
				self.progress = 2
		if self.progress == 2:
			payload = thing.get(self.goal)
			if payload.isvisible():
				dialog.play("firstsatellite3")
				self.progress = 3
		if self.progress == 3:
			if window.distance(state.mother, state.you) < 8:
				dialog.play("firstsatellite4")
				self.progress = 4
		

def think(dt):
	for quest in quests.values():
		quest.think(dt)

Intro()
Act1()

def dump():
	data = {}
	for qname, quest in quests.items():
		data[qname] = quest.dump()
	return data
def load(obj):
	for qname, quest in quests.items():
		quest.load(data[qname])

