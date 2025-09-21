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

class Grid:
	def __init__(self):
		self.nodes = {}
		self.addnode((0, 0))

	def addnode(self, p, parent = None):
		node = Node(p, parent)
		self.nodes[p] = node
		if parent is not None:
			parent.children.append(node)

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
		parent = node.parent
		if parent is not None:
			yield parent.p, node.p

def canaddsegment(segment):
	return grid.canaddsegment(segment)

def addsegment(segment):
	return grid.addsegment(segment)

