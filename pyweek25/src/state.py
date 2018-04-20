from __future__ import division
import math
try:
	import cPickle as pickle
except ImportError:
	import pickle
from . import view, thing


level = """
		x1	x	P	y12	y		
	x	x8	x8	x	.	y	y	
x	x	x8	xX	x	.	yP	y	y
x	x	x	x	x	.	y	y	y
x	x	x	x	P	y	y	y	y
x	x	x	.	y	y	y	y	y
x	x	xP	.	y	yY	y8	y	y
	x	x	.	y	y8	y8	y	
		x	x12	P	y	y		
"""


level = """
y	y	y	y	10	.	.	P
y	.	.	y	10	.	.	.
y	.	.	y	10	.	.	.
yY	.	.	y	10	10	10	10
x	x	x	P	x	x	x	x
x	.	.	y	.	.	.	x
x	.	.	y	.	.	.	x
P	y	y	y	xX	x	x	x
"""

grid = {}
meteors = {}
pieces = {}
parts = {}
statestack = []
def pushstate():
	obj = grid, meteors, pieces, parts
	statestack.append(pickle.dumps(obj, 2))
def popstate():
	global grid, meteors, pieces, parts
	if not statestack:
		return
	obj = pickle.loads(statestack.pop())
	grid, meteors, pieces, parts = obj
def resetstate():
	del statestack[1:]
	popstate()
def turn():
	return len(statestack)

def load():
	for yline, line in enumerate(level.splitlines()):
		for xfield, field in enumerate(line.split("\t")):
			field = field.strip()
			p = x, y = xfield, -yline
			if not field:
				continue
			name = "x" if "x" in field else "y" if "y" in field else "."
			grid[p] = thing.Tile(name = name, color = colors[name], pG = p)
			if "P" in field:
				parts[p] = thing.Part(name = "P", color = "#666666", pG = p)
			for name in "XYZ":
				if name in field:
					pieces[name] = thing.Piece(name = name, color = colors[name.lower()], pG = p)
			field = "".join(c for c in field if c not in "xy.XYZP")
			if field.isdigit():
				meteors[p] = thing.Impact(turn = int(field), pG = p)
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
def getthinkers():
	objs = list(pieces.values()) + list(parts.values()) + list(grid.values()) + list(meteors.values())
	return objs
def gettiles():
	return sorted(grid.values())
def getboardobjs():
	objs = list(pieces.values()) + list(parts.values()) + list(meteors.values())
	return sorted(objs)

# Distance for the purpose of piece movement (i.e. taxicab metric)
def distanceG(p0G, p1G):
	x0G, y0G, _ = view.ifzG(p0G)
	x1G, y1G, _ = view.ifzG(p1G)
	return abs(x0G - x1G) + abs(y0G - y1G)
# Euclidean distance
def edistanceG(p0G, p1G):
	x0G, y0G, _ = view.ifzG(p0G)
	x1G, y1G, _ = view.ifzG(p1G)
	return math.sqrt((x0G - x1G) ** 2 + (y0G - y1G) ** 2)
def isoccupiedG(pG):
	return any(distanceG(piece.pG(), pG) == 0 for piece in pieces.values())
def canmoveto(name, pG):
	if pG not in grid or (name, grid[pG].name) not in canstand:
		return False
	d = distanceG(pieces[name].pG(), pG)
	return d == 1 and not isoccupiedG(pG)
def moveto(name, pG):
	pieces[name].xG, pieces[name].yG = pG

def destroy(pG):
	for objs in [pieces, parts, grid, meteors]:
		for key in [key for key, obj in objs.items() if (obj.xG, obj.yG) == pG]:
			del objs[key]
	for tile in grid.values():
		d = edistanceG(pG, tile.pG())
		tile.jolt(0.1 * d)


