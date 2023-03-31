import math
from functools import lru_cache, cache
from collections import defaultdict
import pygame

adjs = [(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)]
dcorners = [
	((x0 + x1) / 3, (y0 + y1) / 3)
	for (x0, y0), (x1, y1) in
	[(adjs[j-1], adjs[j]) for j in range(6)]
]
angledH = { adj: (60 * j - 60) % 360 for j, adj in enumerate(adjs) }


def vsub(p0, p1):
	x0, y0 = p0
	x1, y1 = p1
	return x0 - x1, y0 - y1

def distanceH(pH0, pH1):
	(xH0, yH0), (xH1, yH1) = pH0, pH1
	dx, dy = xH1 - xH0, yH1 - yH0
	return max(abs(dx), abs(dy), abs(dx + dy))

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
	pHs = [(x0 + dx, y0 + dy) for dx in (0, 1) for dy in (0, 1)]
	return min(pHs, key = lambda pH: math.distance(GconvertH(pH), pG))

@lru_cache(1000)
def GoutlineH(pH):
	x, y = pH
	return [GconvertH((x + dx, y + dy)) for dx, dy in dcorners]
	

@lru_cache(1000)
def neighbors(pH):
	xH, yH = pH
	return [(xH + dxH, yH + dyH) for dxH, dyH in adjs]

class Grid:
	def __init__(self, cells):
		self.cells = set(cells)
		self.reset()

	def reset(self):
		# Currently no lights or obstacles occupying this space.
		self.open = set(self.cells)
		# In the sights of a beam.
		self.lit = set()
		# Occupied by a goal.
		self.goals = set()
		self.walls = { cell: set() for cell in self.cells }
		self.tsetup = 0
		self.nsetup = 0
		self.todo = self.dowork()

	def block(self, pH):
		self.open.remove(pH)
		self.todo = self.dowork()

	def addgoal(self, pH):
		self.goals.add(pH)
		self.todo = self.dowork()

	def illuminate(self, pH):
		self.lit.add(pH)
		self.todo = self.dowork()
	
	def addwall(self, pH0, pH1, bothways=True):
		if pH0 in self.walls:
			self.walls[pH0].add(pH1)
		if bothways:
			self.addwall(pH1, pH0, bothways=False)		

	def pGs(self):
		return [GconvertH(cell) for cell in self.cells]
		
	def killtime(self, dt):
		if not self.todo: return
		t0 = pygame.time.get_ticks() * 0.001
		t1 = t0 + dt
		try:
			while pygame.time.get_ticks() * 0.001 < t1:
				next(self.todo)
		except StopIteration:
			self.todo = None
		self.tsetup += pygame.time.get_ticks() * 0.001 - t0
		self.nsetup += 1
		if self.todo is None:
			print("setup time", self.nsetup, round(self.tsetup, 3))

	def dowork(self):
		yield
		self.neighbors = {}
		self.pathstep = {}
		self.drings = {}
		self.walkable = self.open - self.lit
		for cell in self.walkable:
			self.neighbors[cell] = (self.walkable & set(neighbors(cell))) - self.walls[cell]
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
			if empty:
				break
		self.components = []
		self.componentmap = {}
		toconnect = set(self.walkable)
		while toconnect:
			cell = next(iter(toconnect))
			component = set()
			for dring in self.drings[cell].values():
				component |= dring
				yield
			toconnect -= component
			jcomponent = len(self.components)
			for cell in component:
				self.componentmap[cell] = jcomponent
				yield
			self.components.append(component)

	def getpath(self, p0, p1):
		if self.todo is not None: return None
		p = p0
		path = [p]
		while p != p1:
			p = self.pathstep[(p, p1)][0][0]
			path.append(p)
		return path

	def draw0(self, shading):
		from . import view, pview
		colors = (160, 160, 160), (170, 170, 130), (150, 150, 190)
		sdict = defaultdict(list)
		for scell, f, scolor in shading:
			sdict[scell].append((f, scolor))
		for x, y in self.cells:
			pGs = GoutlineH((x, y))
			pVs = [view.VconvertG(pG) for pG in pGs]
			color = colors[(x - y) % 3]
			for f, scolor in sdict[(x, y)]:
				color = math.imix(color, scolor, f)
			pygame.draw.polygon(pview.screen, color, pVs)

	def drawpath(self, p0, p1):
		path = self.getpath(p0, p1)
		if path is None:
			return
		from . import view, pview, graphics
		pGs = [GconvertH(pH) for pH in path]
		da = (pygame.time.get_ticks() * 0.001 * 3) % 1
		for ja in range(len(pGs) - 1):
			a = ja + da
			n, k = divmod(a, 1)
			n = int(n)
			pG = math.mix(pGs[n], pGs[n+1], k)
			angle = angledH[vsub(path[n+1], path[n])]
			pV = view.VconvertG(pG)
			scale = view.VscaleG * 0.005
			color = 200, 100, 0
			graphics.draw("path", pV, scale, angle = angle, mask = color)

	def samecomponent(self, pH0, pH1):
		if self.todo is not None:
			print("PATHFINDING....", self.nsetup, self.tsetup)
			return False
		return self.componentmap.get(pH0, -1) == self.componentmap.get(pH1, -2)

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



