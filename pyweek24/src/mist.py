from . import pview

class Mist(object):
	def __init__(self, z):
		self.z = z
	def draw(self):
		pview.fill((100, 100, 100, 40))

