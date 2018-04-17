from __future__ import division
import pickle
from . import view, thing


level = """
		x	x	P	y12	y		
	x	x8	x8	x	.	y	y	
x	x	x8	xX	x	.	yP	y	y
x	x	x	x	x	.	y	y	y
x	x	x	x	P	y	y	y	y
x	x	x	.	y	y	y	y	y
x	x	xP	.	y	yY	y8	y	y
	x	x	.	y	y8	y8	y	
		x	x12	P	y	y		
"""

grid = {}
meteors = {}
pieces = {}
parts = {}
statestack = []
def pushstate():
	obj = grid, meteors, pieces, parts
	statestack.append(pickle.dumps(obj))
def popstate():
	global grid, meteors, pieces, parts
	if not statestack:
		return
	obj = pickle.loads(statestack.pop())
	grid, meteors, pieces, parts = obj
def resetstate():
	del statestack[1:]
	popstate()

def load():
	for yline, line in enumerate(level.splitlines()):
		for xfield, field in enumerate(line.split("\t")):
			field = field.strip()
			p = x, y = xfield, -yline
			if not field:
				continue
			grid[p] = "x" if "x" in field else "y" if "y" in field else "."
			if "P" in field:
				parts[p] = thing.Part(name = "P", color = "#666666", xG = x, yG = y)
			for name in "XYZ":
				if name in field:
					pieces[name] = thing.Piece(name = name, color = colors[name.lower()], xG = x, yG = y)
			field = "".join(c for c in field if c not in "xy.XYZP")
			if field.isdigit():
				meteors[p] = int(field)
	xmin = min(x for x, y in grid)
	xmax = max(x for x, y in grid)
	ymin = min(y for x, y in grid)
	ymax = max(y for x, y in grid)
	view.xG0 = (xmin + xmax) / 2
	view.yG0 = (ymin + ymax) / 2

colors = {
	".": "#777777",
	"x": "blue",
	"y": "red",
	"z": "#444444",
}
canstand = set([("X", "x"), ("X", "."), ("Y", "y"), ("Y", ".")])
def gettiles():
	for x, y in sorted(grid, key = view.sortkeyG):
		yield colors[grid[(x, y)]], (x, y)
def getthinkers():
	objs = list(pieces.values()) + list(parts.values())
	return objs
def getboardobjs():
	objs = list(pieces.values()) + list(parts.values())
	return sorted(objs)

def distanceG(p0G, p1G):
	x0G, y0G, _ = view.ifzG(p0G)
	x1G, y1G, _ = view.ifzG(p1G)
	return abs(x0G - x1G) + abs(y0G - y1G)
def isoccupiedG(pG):
	return any(distanceG(piece.pG(), pG) == 0 for piece in pieces.values())
def canmoveto(name, pG):
	if pG not in grid or (name, grid[pG]) not in canstand:
		return False
	d = distanceG(pieces[name].pG(), pG)
	return d == 1 and not isoccupiedG(pG)
def moveto(name, pG):
	pieces[name].xG, pieces[name].yG = pG

