from __future__ import division
from . import view


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
					pieces[char] = x, -y
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
	for name, (x, y) in sorted(pieces.items(), key = lambda kv: view.sortkeyG(kv[1])):
		yield name, colors[name.lower()], (x, y)
