import random, math
from . import state, effects, graphics, thing

# All coordinates in this module are G (grid) coordinates


class Node:
	def __init__(self, p, parent = None):
		self.p = p
		self.ps = [p]
		self.parent = parent
		self.children = []

	def branches(self):
		x, y = self.p
		return [(x, y + 1), (x + 1, y + 1)]

	def segments(self):
		if self.parent is not None:
			yield self.parent.p, self.p

	def canextend(self):
		return not self.children

def adjs(ps):
	for x0, y0 in sorted(ps):
		for x1, y1 in sorted(ps):
			if x1 in (x0, x0 + 1) and y1 == y0 + 1:
				yield (x0, y0), (x1, y1)


class Structure:
	dps = []
	Tincome = 0
	income = 0
	def __init__(self, parent):
		self.parent = parent
		x0, y0 = parent.p
		self.ps = [(x0 + dx, y0 + dy) for dx, dy in self.dps]
		self.p0 = math.vavg(self.ps)
		self.pbase = parent.p
		self.segs = list(adjs([self.pbase] + self.ps))
		self.t = 0
		self.taccum = 0

	def branches(self):
		return []

	def segments(self):
		return []

	def canextend(self):
		return False

	def getincome(self):
		state.earn(self.income)
		effects.addinfoG(self.p0, f"+${self.income}")

	def think(self, dt):
		self.t += dt
		self.taccum += dt
		if self.Tincome:
			while self.taccum >= self.Tincome:
				self.taccum -= self.Tincome
				self.getincome()

	def draw(self):
		graphics.drawstructure(self.pbase, self.ps, self.text, self.color)

class Office(Structure):
	Tincome = 5
	income = 1
	text = "office"
	dps = [(0, 1), (1, 1), (1, 2)]
	color = (70, 60, 40)

class Spire(Structure):
	text = "spire"
	dps = [(0, 1), (1, 1), (1, 2), (1, 3), (2, 3), (2, 4)]
	color = (70, 40, 70)


stypes = {
	"office": Office,
	"spire": Spire,
}


class Grid:
	def __init__(self):
		self.nodes = {}
		self.structures = []
		self.addnode((0, 0))
		self.resetcache()

	def resetcache(self):
		self.LCAcache = {}
		self.stepcache = {}

	def LCA(self, p0, p1):
		if p0 == p1: return p0
		key = p0, p1
		if key not in self.LCAcache:
			x0, y0 = p0
			x1, y1 = p1
			if y0 >= y1:
				p0 = self.nodes[p0].parent.p
			if y1 >= y0:
				p1 = self.nodes[p1].parent.p
			self.LCAcache[key] = self.LCA(p0, p1)
		return self.LCAcache[key]

	def stepto(self, p0, p1):
		if p0 == p1: return None
		key = p0, p1
		if key not in self.stepcache:
			pmin = self.LCA(p0, p1)
			if p1 == pmin:
				self.stepcache[key] = self.nodes[p0].parent.p
			else:
				p1p = self.nodes[p1].parent.p
				self.stepcache[key] = self.stepto(p0, p1p) or p1
		return self.stepcache[key]

	def addnode(self, p, parent = None):
		node = Node(p, parent)
		self.nodes[p] = node
		if parent is not None:
			parent.children.append(node)
		self.resetcache()

	# Returns the structure on True.
	def canaddstructure(self, stypename, p0):
		if p0 not in self.nodes:
			return False
		parent = self.nodes[p0]
		if not parent.canextend():
			return False
		stype = stypes[stypename]
		structure = stype(parent)
		if any(p in self.nodes for p in structure.ps):
			return False
		if not all(state.inbounds(p) for p in structure.ps):
			return False
		return structure

	def addstructure(self, stypename, p0):
		structure = self.canaddstructure(stypename, p0)
		if not structure:
			return False
		for p in structure.ps:
			self.nodes[p] = structure
		if structure.parent is not None:
			structure.parent.children.append(structure)
		self.structures.append(structure)
		self.resetcache()
		return structure

	def addrandomnode(self):
		while True:
			parent = random.choice(list(self.nodes.values()))
			branch = random.choice(parent.branches())
			if branch in self.nodes:
				continue
			self.addnode(branch, parent)
			break

	def canaddsegment(self, segment):
		p0, p1 = segment
		if p1 in self.nodes: return False
		if p0 not in self.nodes: return False
		if not state.inbounds(p1): return False
		return p1 in self.nodes[p0].branches()

	def addsegment(self, segment):
		if not self.canaddsegment(segment):
			return False
		p0, p1 = segment
		self.addnode(p1, self.nodes[p0])
		return True

	def canremoveat(self, p):
		if p not in self.nodes:
			return False
		x, y = p
		if x in [0, y]:  # Don't remove leftmost or rightmost branch.
			return False
		return True

	def removeat(self, p):
		if not self.canremoveat(p): return False
		obj = self.nodes[p]
		if obj.parent is not None:
			obj.parent.children.remove(obj)
		if isinstance(obj, Structure):
			self.structures.remove(obj)
		for p in obj.ps:
			del self.nodes[p]
		self.resetcache()
		return True



grid = Grid()

def segments():
	for node in grid.nodes.values():
		yield from node.segments()

def addsegment(segment):
	return grid.addsegment(segment)

# Return False on failure
def addstructure(stypename, p0):
	grid.addstructure(stypename, p0)

def removeat(p):
	return grid.removeat(p)

def stepto(p0, p1):
	return grid.stepto(p0, p1)

def spawnshopper():
	spires = [obj for obj in grid.structures if isinstance(obj, Spire)]
	offices = [obj for obj in grid.structures if isinstance(obj, Office)]
	if not spires or not offices: return
	state.things.append(thing.Shopper(random.choice(offices), random.choice(spires)))


def think(dt):
	for obj in grid.structures:
		obj.think(dt)

def draw():
	for pG0, pG1 in segments():
		graphics.drawsegment(pG0, pG1)
	for obj in grid.structures:
		obj.draw()


