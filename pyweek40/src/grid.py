import random, math
from . import state, effects

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
		x0, y0 = parent.p
		self.ps = [(x0 + dx, y0 + dy) for dx, dy in self.dps]
		self.p0 = math.vavg(self.ps)
		self.segs = list(adjs([parent.p] + self.ps))
		self.parent = parent
		self.t = 0
		self.taccum = 0

	def branches(self):
		return []

	def segments(self):
		return self.segs

	def canextend(self):
		return False

	def getincome(self):
		state.earn(self.income)
		effects.addinfo(self.p0, f"+${self.income}")

	def think(self, dt):
		self.t += dt
		self.taccum += dt
		if self.Tincome:
			while self.taccum >= self.Tincome:
				self.taccum -= self.Tincome
				self.getincome()
		

class Office(Structure):
	Tincome = 5
	income = 1
	dps = [(0, 1), (1, 1), (1, 2)]

class Spire(Structure):
	dps = [(0, 1), (1, 1), (1, 2), (1, 3), (2, 3), (2, 4)]

stypes = {
	"office": Office,
	"spire": Spire,
}


class Grid:
	def __init__(self):
		self.nodes = {}
		self.structures = []
		self.addnode((0, 0))

	def addnode(self, p, parent = None):
		node = Node(p, parent)
		self.nodes[p] = node
		if parent is not None:
			parent.children.append(node)

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

	def removeat(self, p):
		if p not in self.nodes:
			return False
		x, y = p
		if x in [0, y]:  # Don't remove leftmost or rightmost branch.
			return False
		obj = self.nodes[p]
		if obj.parent is not None:
			obj.parent.children.remove(obj)
		if isinstance(obj, Structure):
			self.structures.remove(obj)
		for p in obj.ps:
			del self.nodes[p]
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

def think(dt):
	for obj in grid.structures:
		obj.think(dt)


