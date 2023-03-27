import math
from functools import lru_cache, cache
import pygame

adjs = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
dcorners = [
	((x0 + x1) / 3, (y0 + y1) / 3)
	for (x0, y0), (x1, y1) in
	[(adjs[j-1], adjs[j]) for j in range(6)]
]

def GconvertH(pH):
	xH, yH = pH
	xG = 1.5 * xH
	yG = math.sqrt(3) * (yH + 0.5 * xH)
	return xG, yG

def HconvertG(pG):
	xG, yG = pG
	xH = xG / 1.5
	yH = yG / math.sqrt(3) - 0.5 * xH
	return xH, yH

def HnearestG(pG):
	xH, yH = HconvertG(pG)
	x0 = math.floor(xH)
	y0 = math.floor(yH)
	pHs = [(x0 + dx, y0 + dy) for dx in (0, 1) for y in (0, 1)]
	return min(pHs, key = lambda pH: math.hypot(GconvertH(pH), pG))
	

@lru_cache(1000)
def neighbors(pH):
	xH, yH = pH
	return [(xH + dxH, yH + dyH) for dxH, dyH in adjs]

class Grid:
	def __init__(self, cells):
		self.cells = set(cells)
		self.todo = self.dowork()
		self.tsetup = 0
		self.setup = False

	def pGs(self):
		return [GconvertH(cell) for cell in self.cells]
		
	def killtime(self, dt):
		if self.setup: return
		t0 = pygame.time.get_ticks() * 0.001
		t1 = t0 + dt
		try:
			while pygame.time.get_ticks() * 0.001 < t1:
				next(self.todo)
		except StopIteration:
			self.setup = True
		self.tsetup += pygame.time.get_ticks() * 0.001 - t0

	def dowork(self):
		self.neighbors = {}
		self.pathstep = {}
		self.drings = {}
		for cell in self.cells:
			self.neighbors[cell] = self.cells & set(neighbors(cell))
			self.pathstep[(cell, cell)] = [], 0
			self.drings[cell] = { 0: set([cell]) }
			yield
		for d in range(1, len(self.cells)):
			empty = True
			for cell, ns in self.neighbors.items():
				dcells = set(cell for n in ns for cell in self.drings[n][d-1])
				dcells -= self.drings[cell][d-1]
				if d > 1:
					dcells -= self.drings[cell][d-2]
				self.drings[cell][d] = dcells
				for dcell in dcells:
					dns = [n for n in ns if dcell in self.drings[n][d-1]]
					self.pathstep[(cell, dcell)] = dns, d
					yield
				if dcells:
					empty = False
				yield
			if empty:
				break

	def getpath(self, p0, p1):
		if not self.setup: return None
		p = p0
		path = [p]
		while p != p1:
			p = self.pathstep[(p, p1)][0][0]
			path.append(p)
		return path

	def draw0(self):
		from . import view, pview
		colors = (220, 220, 220), (210, 210, 240), (200, 200, 255)
		for x, y in cells:
			pHs = [(x + dx, y + dy) for dx, dy in dcorners]
			pVs = [view.VconvertG(GconvertH(pH)) for pH in pHs]
			color = colors[(x - y) % 3]
			pygame.draw.polygon(pview.screen, color, pVs)
			
if __name__ == "__main__":
	from . import pview, view
	pygame.init()
	view.init()
	cells = [(x, y) for x in range(-4, 5) for y in range(-4, 5)]
	grid = Grid(cells)
	view.framegrid(grid)
	grid.killtime(5)
	print(grid.setup, grid.tsetup)
	while not any(event.type == pygame.KEYDOWN for event in pygame.event.get()):
		pview.fill((0, 0, 0))
		grid.draw0()
		pygame.display.flip()



