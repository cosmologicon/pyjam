from . import settings, state, thing

def getcstate(estate):
	return {}

def onpush():
	state.state.things.append(thing.You(pos = [0, 0, 1]))
	state.state.things.append(thing.You(pos = [5, 5, 1]))

def think(dt, estate):
	cstate = getcstate(estate)
	state.state.think(dt)

def draw():
	state.state.draw()


