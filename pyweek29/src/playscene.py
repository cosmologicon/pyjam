import pygame, statistics, math
from . import pview, view, thing, state, settings, scene, control, level, progress
from .pview import T

class self:
	pass

def init():
	level.load()
	self.alpha = 1

def control(keys):
	if not state.winning():
		state.you.control(keys)

def think(dt):
	if state.winning():
		kdowns = set()
		self.alpha = math.approach(self.alpha, 1, 4 * dt)
		if self.alpha == 1:
			scene.pop()
			progress.beat(progress.at)
	else:
		self.alpha = math.approach(self.alpha, 0, 4 * dt)
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
		if 0 <= lep.y < state.h:
			lep.draw()
	if state.held:
		state.held.draw()

	# Right panel
	pview.fill((80, 80, 100, 220), T(view.rrect))
	for p0, p1 in gridlines:
		pygame.draw.line(pview.screen, (255, 0, 255), view.worldtomap(p0), view.worldtomap(p1), T(1))
	state.you.drawmap()
	for lep in state.leps:
		if 0 <= lep.y < state.h:
			lep.drawmap()
	mcenter = T(view.rrect.centerx, 70)
	pygame.draw.circle(pview.screen, (255, 200, 80), mcenter, T(50), T(2))
	pygame.draw.circle(pview.screen, (255, 200, 80), mcenter, T(50 * state.you.jumpmeter()))
	for j in range(state.maxleaps):
		pos = T(view.rrect.centerx + 60 * (-(state.maxleaps - 1) / 2 + j), 160)
		if j < state.leaps:
			pygame.draw.circle(pview.screen, (255, 200, 80), pos, T(24))
		else:
			pygame.draw.circle(pview.screen, (255, 200, 80), pos, T(24), T(2))

	if self.alpha:
		pview.fill((255, 255, 255, int(255 * self.alpha)))


