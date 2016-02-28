from . import settings, state, thing, background, window

def getcstate(estate):
	return {}

def onpush():
	state.state.things.append(thing.You(pos = [5, 5, 10]))
	state.state.things[-1].settarget((-10, 0))

def think(dt, estate):
	cstate = getcstate(estate)
	state.state.think(dt)
	window.snapto(state.state.things[-1])

def draw():
	background.draw()
	state.state.draw()


