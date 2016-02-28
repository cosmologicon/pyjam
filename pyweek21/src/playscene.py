from . import settings, state, thing, background, window, gamedata

def getcstate(estate):
	return {}


assembling = False
curtain = -1
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
	global assembling, curtain
	if estate["lclick"]:
		x, y = window.screentoworld(*estate["mpos"])
#		building = thing.Building(pos = [x, y, 0])
#		state.state.ships[-1].setbuildtarget(building)
		if state.state.cursor:
			state.state.cursor.settarget((x, y))
			state.state.effects.append(thing.GoIndicator(pos = [x, y, 0]))
	if estate["rclick"]:
		x, y = window.screentoworld(*estate["mpos"])
		window.targetpos(x, y)
	if estate["cycle"]:
		ship = state.state.nextcursor()
		state.state.cursor = ship
		window.targetpos(ship.x, ship.y, ship.z)
	if estate["assemble"] and not assembling and curtain == 1:
		assembling = True

	if assembling:
		curtain -= 6 * dt
		if curtain < -0.5:
			state.state.assemble(window.x0, window.y0)
			assembling = False
	else:
		curtain = min(curtain + 6 * dt, 1)

	state.state.think(dt)
	window.think(dt)
#	window.snapto(state.state.things[-1])

def draw():
	background.draw()
	state.state.draw()
#	background.drawclouds()
	if curtain <= 0:
		window.screen.fill((0, 0, 0))
	elif curtain < 1:
		h = int(window.sy / 2 * (1 - curtain))
		window.screen.fill((0, 0, 0), (0, 0, window.sx, h))
		window.screen.fill((0, 0, 0), (0, window.sy - h, window.sx, h))

