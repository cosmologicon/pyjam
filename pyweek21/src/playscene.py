from . import settings, state, thing, background, window

def getcstate(estate):
	return {}

def onpush():
	state.state.ships.append(thing.You(pos = [5, 5, 10]))

def think(dt, estate):
	if estate["lclick"]:
		x, y = window.screentoworld(*estate["mpos"])
		building = thing.Building(pos = [x, y, 0])
		state.state.ships[-1].setbuildtarget(building)
	if estate["rclick"]:
		x, y = window.screentoworld(*estate["mpos"])
		window.targetpos(x, y)
	if estate["cycle"]:
		ship = state.state.ships[-1]
		window.targetpos(ship.x, ship.y, ship.z)

	state.state.think(dt)
	window.think(dt)
#	window.snapto(state.state.things[-1])

def draw():
	background.draw()
	state.state.draw()


