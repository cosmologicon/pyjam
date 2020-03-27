import pygame, statistics, math
from . import pview, view, thing, state, settings, scene, control, level, progress, sound
from . import draw as D
from .pview import T

class self:
	pass

def init():
	level.load()
	self.alpha = 1
	self.losing = False
	self.lepdtf = 1
	t0 = pygame.time.get_ticks()
	D.finishkill()
	

def control(keys):
	if "forfeit" in keys:
		self.losing = True
	if not state.winning() and not self.losing:
		state.you.control(keys)

def think(dt):
	if state.winning() or self.losing:
		kdowns = set()
		self.alpha = math.approach(self.alpha, 1, 4 * dt)
		if self.alpha == 1:
			scene.pop()
			if state.winning():
				progress.beat(progress.at)
	else:
		self.alpha = math.approach(self.alpha, 0, 4 * dt)
	state.you.think(dt)
	self.lepdtf = math.approach(self.lepdtf, (0.1 if state.you.state == "jumping" else 1), 4 * dt)
	for lep in state.leps:
		lep.think(dt * self.lepdtf)
	for lep in state.goals:
		lep.think(dt * self.lepdtf)
	view.think(dt)

def draw():
	D.background("lake.jpg")
	gridlines = [((x, 0), (x, state.h)) for x in range(0, state.w + 1)]
	gridlines += [((0, y), (state.w, y)) for y in range(0, state.h + 1)]
	if state.you.state == "jumping":
		for p0, p1 in gridlines:
			pygame.draw.line(pview.screen, (50, 50, 140),
				view.worldtoscreen(p0), view.worldtoscreen(p1), T(1))
	state.you.draw()
	for lep in state.goals:
		lep.draw()
	(xmin, xmax), (ymin, ymax) = view.visiblerange()
	for lep in state.leps:
		if xmin <= lep.x <= xmax and ymin <= lep.y <= ymax:
			lep.draw()
	if state.held:
		state.held.draw()

	# Right panel
	pview.fill((80, 80, 100, 220), T(view.rrect))
	for p0, p1 in gridlines:
		pygame.draw.line(pview.screen, (100, 60, 120), view.worldtomap(p0), view.worldtomap(p1), T(1))
	state.you.drawmap()
#	for lep in state.leps:
#		lep.drawmap()
#	for lep in state.leps:
#		lep.drawarrowmap()
	mcenter = T(view.rrect.centerx, 70)
	if False:
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


