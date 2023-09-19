import random, math, pygame
from . import state, thing, view, graphics
from . import pview
from .pview import T


def init():
	state.you = thing.You((0, 0))
	state.DMs = [
#		thing.Orbiter((0, 0), j * math.tau / 3, 0.3, 5, 0.4)
#		for j in range(3)
	]
	for _ in range(10):
		pos0 = math.CS(random.uniform(0, math.tau), random.uniform(0, 5))
		Rorbit = random.uniform(10, 20)
		pos1 = math.CS(random.uniform(0, math.tau), random.uniform(60, 100))
		v = random.uniform(1, 3)
		Nstay = random.randint(10, 20)
		reverse = random.choice([False, True])
		state.DMs += [thing.Visitor(pos0, pos1, Nstay, Rorbit, v, reverse=reverse)]
	for _ in range(100):
		pos0 = math.CS(random.uniform(0, math.tau), random.uniform(0, 50))
		Rorbit = random.uniform(60, 100)
		v = random.uniform(1, 3)
		reverse = random.choice([False, True])
		r = random.uniform(0.4, 1)
		state.DMs += [thing.CircleRock(pos0, Rorbit, v, r, reverse)]
	state.pulses = []
	state.tracers = []
	state.spawners = []
	state.shots = []


def think(dt, kdowns = [], kpressed = [0] * 128):
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
	for shot in state.shots:
		shot.think(dt)
	state.pulses = [pulse for pulse in state.pulses if pulse.alive]
	state.tracers = [tracer for tracer in state.tracers if tracer.alive]
	state.shots = [shot for shot in state.shots if shot.alive]
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
	for shot in state.shots:
		shot.draw()
	state.you.draw()
#	drawmap()


def drawmap():
	mradius = 500
	mrect = T(pygame.Rect(0, 0, 640, 640))
	def MconvertG(pos):
		x, y = pos
		return pview.T(640 + 320 / mradius * x, 360 - 320 / mradius * y)
	mrect.center = pview.center
	pview.screen.fill((10, 10, 10), mrect)
	for DM in state.DMs:
		pM = MconvertG(DM.pos)
		pygame.draw.circle(pview.screen, (0, 0, 0), pM, T(3))
		pygame.draw.circle(pview.screen, (0, 255, 255), pM, T(3), T(1))
	pygame.draw.circle(pview.screen, (255, 0, 0), MconvertG(state.you.pos), T(5))


