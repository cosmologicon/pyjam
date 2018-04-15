from __future__ import division
from . import view, thing


level = """
zzZz
zzzz
xxyy
XxyY
xxyy
"""

grid = {}
pieces = {}
def load():
	for y, line in enumerate(level.splitlines()):
		for x, char in enumerate(line):
			if char.strip():
				grid[(x, -y)] = char.strip().lower()
				if char.isupper():
					pieces[char] = thing.Piece(name = char, color = colors[char.lower()], xG = x, yG = -y)
	xmin = min(x for x, y in grid)
	xmax = max(x for x, y in grid)
	ymin = min(y for x, y in grid)
	ymax = max(y for x, y in grid)
	view.xG0 = (xmin + xmax) / 2
	view.yG0 = (ymin + ymax) / 2

colors = {
	"x": "blue",
	"y": "red",
	"z": "gray",
}
def gettiles():
	for x, y in sorted(grid, key = view.sortkeyG):
		yield colors[grid[(x, y)]], (x, y)
def getpieces():
	return sorted(pieces.values())

def distanceG(p0G, p1G):
	x0G, y0G, _ = view.ifzG(p0G)
	x1G, y1G, _ = view.ifzG(p1G)
	return max(abs(x0G - x1G), abs(y0G - y1G))
def isoccupiedG(pG):
	return any(distanceG(piece.pG(), pG) == 0 for piece in pieces.values())
def canmoveto(name, pG):
	d = distanceG(pieces[name].pG(), pG)
	return d == 1 and not isoccupiedG(pG)
def moveto(name, pG):
	pieces[name].xG, pieces[name].yG = pG

