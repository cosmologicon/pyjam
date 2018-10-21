from . import view, state, thing, graphics

def init():
	state.you = thing.You()

def think(dt, kpressed, kdowns):
	pass

def draw():
	view.clear((0.1, 0.1, 0.1, 1))
	view.look()
	graphics.drawwater()


