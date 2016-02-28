from . import settings, state, thing, background, window, gamedata

def getcstate(estate):
	return {}

def onpush():
	x, y = gamedata.data["start"]
	you = thing.You(pos = [x, y, 4])
	state.state.addtoteam(you)
	x, y = gamedata.data["beta"]
	state.state.addtoteam(thing.You(pos = [x, y, 4]))
	window.snapto(you)
	for x, y in gamedata.data["activated"]:
		building = thing.Building(pos = [x, y, 0], needpower = 10)
		state.state.addbuilding(building)

def think(dt, estate):
	if estate["lclick"]:
		x, y = window.screentoworld(*estate["mpos"])
#		building = thing.Building(pos = [x, y, 0])
#		state.state.ships[-1].setbuildtarget(building)
		if state.state.cursor:
			state.state.cursor.settarget((x, y))
	if estate["rclick"]:
		x, y = window.screentoworld(*estate["mpos"])
		window.targetpos(x, y)
	if estate["cycle"]:
		ship = state.state.nextcursor()
		state.state.cursor = ship
		window.targetpos(ship.x, ship.y, ship.z)

	state.state.think(dt)
	window.think(dt)
#	window.snapto(state.state.things[-1])

def draw():
	background.draw()
	state.state.draw()
#	background.drawclouds()


