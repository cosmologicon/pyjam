from functools import lru_cache
import pygame

adjs = [(1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1)]

@lru_cache(1000)
def neighbors0(pH):
	xH, yH = pH
	return [(xH + dxH, yH + dyH) for dxH, dyH in adjs]
def neighbors(pH):
	return neighbors0(tuple(pH))

class Grid:
	def __init__(self, cells):
		self.cells = set(cells)
		self.todo = self.dowork()
		self.tsetup = 0
		self.setup = False
		
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
		
			
if __name__ == "__main__":
	pygame.init()
	cells = [(x, y) for x in range(-12, 13) for y in range(-12, 13)]
	grid = Grid(cells)
	grid.killtime(5)
	print(grid.setup, grid.tsetup)
	print(grid.getpath((-2, 7), (10, -4)))

