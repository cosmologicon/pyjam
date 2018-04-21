from __future__ import print_function
from . import maff, state

# Returns: pstartG -> number of steps, next step
cache = {}
def distances(board, meteors, pend, name):
	key = board, meteors, pend, name
	if key in cache:
		return cache[key]
	steps = { pstart: [] for pstart, _ in board }
	colors = { pstart: color for pstart, color in board }
	meteors = dict(meteors)
	canmoveto = lambda p: p in colors and (name, colors[p]) in state.canstand
	canclaim = lambda p: p in colors and ((name, colors[p]) in state.cantake or canmoveto(p))
	if not canclaim(pend):
		cache[key] = { p: None for p in steps }
		return cache[key]
	n = 0 if canmoveto(pend) else 1
	turnby = meteors.get(pend, 9999) - n
	steps[pend] = [(turnby, n, None)]
	def combinesteps(step, oldsteps):
		if oldsteps is None:
			return [step], True
		newsteps = set([step] + oldsteps)
		newsteps = [(t0, n0, p0) for t0, n0, p0 in newsteps
			if all((t0, n0) == (t1, n1) or t0 > t1 or n0 < n1
				for t1, n1, p1 in newsteps)]
		newsteps = sorted(newsteps)
		return newsteps, newsteps != oldsteps
	q = [pend]
	while q:
		pcheck = q.pop(0)
		for turnby0, n0, _ in steps[pcheck]:
			for pby in state.neighbors(pcheck):
				if canmoveto(pby):
					n = n0 + 1
					turnby = turnby0 - 1
				elif canclaim(pby):
					n = n0 + 2
					turnby = turnby0 - 2
				else:
					continue
				turnby = min(turnby, meteors.get(pby, 9999))
				if turnby <= (0 if canmoveto(pcheck) else 1):
					continue
				step = turnby, n, pcheck
				newsteps, new = combinesteps(step, steps.get(pby))
#				print(step, steps.get(pby), newsteps, new)
				if new:
					steps[pby] = newsteps
					q.append(pby)
	cache[key] = { p: (min((n, pto) for _, n, pto in s) if s else None) for p, s in steps.items() }
	return cache[key]

def find(who, ptarget):
	board = tuple(sorted((pG, tile.name) for pG, tile in state.grid.items()))
	meteors = tuple(sorted((pG, impact.turn - state.turn()) for pG, impact in state.meteors.items()))
	steps = distances(board, meteors, ptarget, who.name)
	print(steps, steps[(who.xG, who.yG)])
	return steps[(who.xG, who.yG)]

def clear():
	global cache
	cache = {}

if __name__ == "__main__":
	board = tuple(((x, 0), "y") for x in range(6))
	meteors = (((3, 0), 3),)
	for k, v in sorted(distances(board, meteors, (5, 0), "Y").items()):
		print(k, v)
	print()

	board = tuple(((x, 0), ".") for x in range(6))
	meteors = (((3, 0), 5),)
	for k, v in sorted(distances(board, meteors, (5, 0), "Y").items()):
		print(k, v)
	print()

	board = ((0, 0), "y"), ((1, 0), "."), ((2, 0), ".")
	meteors = (((0, 0), 2),)
	for k, v in sorted(distances(board, meteors, (2, 0), "Y").items()):
		print(k, v)
	print()



	board = tuple(((x, y), "y") for x, y in [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (3, 1), (0, 2), (1, 2), (2, 2), (3, 2)])
	meteors = (((2, 0), 3),)
	for k, v in sorted(distances(board, meteors, (3, 0), "Y").items()):
		print(k, v)

