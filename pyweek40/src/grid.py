import random

# All coordinates in this module are G (grid) coordinates


class Node:
	def __init__(self, p, parent = None):
		self.p = p
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
	def __init__(self, parent):
		x0, y0 = parent.p
		self.ps = [(x0 + dx, y0 + dy) for dx, dy in self.dps]
		self.segs = list(adjs([parent.p] + self.ps))
		self.parent = parent

	def branches(self):
		return []

	def segments(self):
		return self.segs

	def canextend(self):
		return False

class Office(Structure):
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
		self.addnode((0, 0))
		self.structures = []

	def addnode(self, p, parent = None):
		node = Node(p, parent)
		self.nodes[p] = node
		if parent is not None:
			parent.children.append(node)

	def addstructure(self, structure):
		for p in structure.ps:
			self.nodes[p] = structure
		if structure.parent is not None:
			structure.parent.children.append(structure)
		self.structures.append(structure)

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
		return p1 in self.nodes[p0].branches()

	def addsegment(self, segment):
		p0, p1 = segment
		self.addnode(p1, self.nodes[p0])


grid = Grid()
for _ in range(10):
	grid.addrandomnode()


def segments():
	for node in grid.nodes.values():
		yield from node.segments()

def canaddsegment(segment):
	return grid.canaddsegment(segment)

def addsegment(segment):
	return grid.addsegment(segment)

# Return False on failure
def addstructure(stypename, p0):
	if p0 not in grid.nodes:
		return False
	parent = grid.nodes[p0]
	if not parent.canextend():
		return False
	stype = stypes[stypename]
	structure = stype(parent)
	if any(p in grid.nodes for p in structure.ps):
		return False
	grid.addstructure(structure)



