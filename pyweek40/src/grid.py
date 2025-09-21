import random

class Node:
	def __init__(self, pG, parent = None):
		self.pG = pG
		self.parent = parent
		self.children = []

	def branches(self):
		xG, yG = self.pG
		return [(xG, yG + 1), (xG + 1, yG + 1)]

class Grid:
	def __init__(self):
		self.nodes = {}
		self.addnode((0, 0))

	def addnode(self, pG, parent = None):
		node = Node(pG, parent)
		self.nodes[pG] = node
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


grid = Grid()
for _ in range(1000):
	grid.addrandomnode()


def segments():
	for node in grid.nodes.values():
		parent = node.parent
		if parent is not None:
			yield parent.pG, node.pG

