import math
from . import window, ptext, state
from .enco import Component
from .util import F

class WorldBound(Component):
	def __init__(self):
		self.x, self.y, self.z = 0, 0, 0
	def init(self, obj):
		if "pos" in obj:
			self.x, self.y, self.z = obj["pos"]
	def screenpos(self, dz = 0):
		return window.worldtoscreen(self.x, self.y, self.z + dz)

class DrawName(Component):
	def __init__(self, hoverdz = 0):
		self.hoverdz = hoverdz
	def draw(self):
		pos = self.screenpos(dz = self.hoverdz * math.sin(2 * self.t))
		ptext.draw(self.__class__.__name__, center = pos, color = "red", fontsize = F(24), owidth = 1)

class ApproachesTarget(Component):
	def __init__(self, speed = 2):
		self.target = None
		self.speed = speed
	def settarget(self, target):
		self.target = target
	def think(self, dt):
		if not self.target:
			return
		dx = self.target[0] - self.x
		dy = self.target[1] - self.y
		d = self.speed * dt
		f = d / math.sqrt(dx ** 2 + dy ** 2)
		if f >= 1:
			self.x, self.y = self.target
			self.target = None
		else:
			self.x += f * dx
			self.y += f * dy

class BuildTarget(Component):
	def __init__(self):
		self.btarget = None
	def setbuildtarget(self, btarget):
		self.target = btarget.x, btarget.y
		self.btarget = btarget
	def think(self, dt):
		if self.btarget and not self.target:
			state.state.buildings.append(self.btarget)
			self.btarget = None

@WorldBound()
class Thing(object):
	def __init__(self, **kwargs):
		self.init(kwargs)
		self.t = 0
	def draw(self):
		pass
	def think(self, dt):
		self.t += dt

@DrawName(0.5)
@ApproachesTarget()
@BuildTarget()
class You(Thing):
	pass

@DrawName()
class Building(Thing):
	pass


