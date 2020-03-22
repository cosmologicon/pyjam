import pygame, statistics, math
from . import pview, view, thing, state, settings, scene, control
from .pview import T

class self:
	pass

def init():
	state.w = 4
	state.h = 6
	state.thang = 1
	state.maxleaps = 1
	state.ngoal = 0
	state.you = thing.You()
	state.leps = [
		thing.Lep((1, 2), [(1, 1)]),
		thing.Lep((2, 1), [(0, 1)]),
		thing.Lep((3, 3), [(0, 1)]),
		thing.GoalLep((1, 4)),
	]
	state.held = None
	self.winning = False
	self.alpha = 1

def control(keys):
	state.you.control(keys)

def think(dt):
	self.winning = state.ngoal >= 1
	if self.winning:
		kdowns = set()
		self.alpha = math.approach(self.alpha, 1, 5 * dt)
		if self.alpha == 1:
			scene.pop()
	else:
		self.alpha = math.approach(self.alpha, 0, 5 * dt)
	state.you.think(dt)
	view.think(dt)

def draw():
	pview.fill((40, 40, 120))
	gridlines = [((x, 0), (x, state.h)) for x in range(0, state.w + 1)]
	gridlines += [((0, y), (state.w, y)) for y in range(0, state.h + 1)]
	for p0, p1 in gridlines:
		pygame.draw.line(pview.screen, (255, 0, 255), view.worldtoscreen(p0), view.worldtoscreen(p1), T(1))
	state.you.draw()
	for lep in state.leps:
		lep.draw()

	# Right panel
	pview.fill((80, 80, 100, 220), T(pygame.Rect(1280 - 240, 0, 240, 720)))
	for p0, p1 in gridlines:
		pygame.draw.line(pview.screen, (255, 0, 255), view.worldtomap(p0), view.worldtomap(p1), T(1))
	state.you.drawmap()
	for lep in state.leps:
		lep.drawmap()
	mcenter = T(1280 - 120, 70)
	pygame.draw.circle(pview.screen, (255, 200, 80), mcenter, T(50), T(2))
	pygame.draw.circle(pview.screen, (255, 200, 80), mcenter, T(50 * state.you.jumpmeter()))
	for j in range(state.maxleaps):
		pos = T(1280 - 120 + 60 * ((state.maxleaps - 1) / 2 + j), 160)
		if j < state.leaps:
			pygame.draw.circle(pview.screen, (255, 200, 80), pos, T(24))
		else:
			pygame.draw.circle(pview.screen, (255, 200, 80), pos, T(24), T(2))

	if self.alpha:
		pview.fill((255, 255, 255, int(255 * self.alpha)))


