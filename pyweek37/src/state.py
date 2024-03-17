import random, pygame, math
from . import grid, view, pview

class Path:
	def __init__(self, pH0):
		self.pHs = [pH0]
		self.color = [random.randint(20, 60) for _ in range(3)]
	def nexts(self):
		return [pH for pH in grid.HadjsH(self.pHs[-1]) if pH not in self.pHs and pH in free]
	def cango(self, pH):
		return pH in self.nexts()
	def add(self, pH):
		self.pHs.append(pH)
	def draw(self, glow = False):
		pDs = [view.DconvertG(grid.GconvertH(pH)) for pH in self.pHs]
		color = math.imix(self.color, (255, 255, 255), 0.5) if glow else self.color
		for pD in pDs:
			pygame.draw.circle(pview.screen, color, pD, view.DscaleG(0.2))
		if len(pDs) >= 2:
			pygame.draw.lines(pview.screen, color, False, pDs, view.DscaleG(0.1))
		

free = set(grid.Hrect(5))

paths = []
planets = []


def addplanet(pH):
	planets.append(pH)
	free.remove(pH)
