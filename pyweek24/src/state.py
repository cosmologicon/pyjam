from . import view

boards = {}
crosscoords = {}
blocks = []

def addboard(board):
	boards[board.name] = board

def think(dt):
	view.X0 += 12 * dt
	you.think(dt)

def resolve():
	global crosscoords, crossings
	p0 = view.to0plane(you.x, you.y, you.z)
	newcrosscoords = { name: board.crosspos(p0) for name, board in boards.items() }
	crossings = []
	for name, (a1, b1) in newcrosscoords.items():
		if name not in crosscoords:
			continue
		a0, b0 = crosscoords[name]
		if b0 > 0 and b1 <= 0:
			crossings.append((name, a0, b0, a1, b1))
	crosscoords = newcrosscoords
	you.resolve()

