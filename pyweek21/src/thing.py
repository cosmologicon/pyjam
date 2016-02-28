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
		ptext.draw(self.__class__.__name__, center = self.screenpos(), color = "red", fontsize = F(16))


@WorldBound()
class Thing(object):
	def __init__(self, **kwargs):
		self.init(kwargs)
	def draw(self):
		pass
	def think(self, dt):
		pass

@DrawName()
class You(Thing):
	pass		
