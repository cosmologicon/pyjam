import random, math
from . import state, thing, view, graphics
from . import pview


def init():
	state.you = thing.You((0, 0))
	state.DMs = [
		thing.Orbiter((0, 0), j * math.tau / 3, 0.3, 5, 0.4)
		for j in range(3)
	]
	state.pulses = []
	state.tracers = []
	state.spawners = []


def think(dt, kdowns, kpressed):
	state.you.control(kdowns, kpressed)
	state.you.think(dt)
	for pulse in state.pulses:
		pulse.think(dt)
	for spawner in state.spawners:
		spawner.think(dt)
	for DM in state.DMs:
		DM.think(dt)
	for tracer in state.tracers:
		tracer.think(dt)
	state.pulses = [pulse for pulse in state.pulses if pulse.alive]
	state.tracers = [tracer for tracer in state.tracers if tracer.alive]
	view.xG0, view.yG0 = state.you.pos


def draw():
	pview.fill((20, 20, 20))
	pview.fill((0, 0, 0))
	graphics.drawnebula()
	graphics.drawstars()

	for pulse in state.pulses:
		pulse.draw()
	for DM in state.DMs:
		DM.draw()
	for tracer in state.tracers:
		tracer.draw()
	state.you.draw()

