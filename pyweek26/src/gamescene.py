from . import view, state, thing, graphics, settings

def init():
	state.you = thing.You()

def think(dt, kpressed, kdowns):
	dx = kpressed["right"] - kpressed["left"]
	dy = kpressed["up"] - kpressed["down"]
	state.you.move(dt, dx, dy)
	state.you.think(dt)

	# Flow
	# TODO: apply to all entities
	state.you.pos.y -= 10 * dt

def draw():
	view.clear((0.1, 0.1, 0.1, 1))
	view.look()
	
	graphics.drawwater()
	graphics.drawyou()


