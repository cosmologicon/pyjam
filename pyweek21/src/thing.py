import math
from . import window, ptext
from .enco import Component
from .util import F

class WorldBound(Component):
	def __init__(self):
		self.x, self.y, self.z = 0, 0, 0
	def init(self, obj):
		if "pos" in obj:
			self.x, self.y, self.z = obj["pos"]
	def screenpos(self):
		return window.worldtoscreen(self.x, self.y, self.z)

class DrawName(Component):
	def draw(self):
		ptext.draw(self.__class__.__name__, center = self.screenpos(), color = "red", fontsize = F(18), ocolor = "black")

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

@WorldBound()
class Thing(object):
	def __init__(self, **kwargs):
		self.init(kwargs)
	def draw(self):
		pass
	def think(self, dt):
		pass

@DrawName()
@ApproachesTarget()
class You(Thing):
	pass		
