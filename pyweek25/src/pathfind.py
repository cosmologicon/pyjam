from . import state

# Returns: pstartG -> number of steps, next step
cache = {}
def distances(board, pend, name):
	key = board, pend, name
	if key in cache:
		return cache[key]
	steps = { pstart: None for pstart, _ in board }
	cache[key] = steps
	colors = { pstart: color for pstart, color in board }
	canmoveto = lambda p: p in colors and (name, colors[p]) in state.canstand
	canclaim = lambda p: p in colors and ((name, colors[p]) in state.cantake or canmoveto(p))
	if not canclaim(pend):
		return steps
	steps[pend] = (0 if canmoveto(pend) else 1), None
	q = [pend]
	while q:
		pcheck = q.pop(0)
		n0, _ = steps[pcheck]
		for pby in state.neighbors(pcheck):
			if canmoveto(pby):
				n = n0 + 1
			elif canclaim(pby):
				n = n0 + 2
			else:
				continue
			if steps[pby] is None or steps[pby][0] > n:
				steps[pby] = n, pcheck
				q.append(pby)
	return steps

def find(who, ptarget):
	board = tuple(sorted((pG, tile.name) for pG, tile in state.grid.items()))
	steps = distances(board, ptarget, who.name)
	return steps[(who.xG, who.yG)]

def clear():
	global cache
	cache = {}
