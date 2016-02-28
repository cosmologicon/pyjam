from . import settings, state, thing, background, window, gamedata

def getcstate(estate):
	return {}

def onpush():
	x, y = gamedata.data["start"]
	you = thing.You(pos = [x, y, 10])
	state.state.ships.append(you)
	window.snapto(you)
	for x, y in gamedata.data["activated"]:
		building = thing.Building(pos = [x, y, 0])
		state.state.buildings.append(building)

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


