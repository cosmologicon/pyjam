import pygame, statistics, math
from . import pview, view, thing, state, settings, scene
from .pview import T

class self:
	pass

def init():
	state.w = 10
	state.h = 10
	state.thang = 1
	state.maxleaps = 1
	state.ngoal = 0
	state.you = thing.You()
	state.leps = [
		thing.Lep((1, 2), [(0, 1)]),
		thing.Lep((2, 1), [(0, 1)]),
		thing.Lep((3, 3), [(0, 1)]),
		thing.GoalLep((4, 4)),
	]
	state.held = None
	self.tcombo = 0
	self.ckeys = set()
	self.tspan = 0
	self.winning = False
	self.alpha = 1

def think(dt, kdowns):
	self.winning = state.ngoal >= 1
	if self.winning:
		kdowns = set()
		self.alpha = math.approach(self.alpha, 1, 5 * dt)
		if self.alpha == 1:
			scene.pop()
	else:
		self.alpha = math.approach(self.alpha, 0, 5 * dt)
	if pygame.K_SPACE in kdowns:
		state.you.control([pygame.K_SPACE])
		if self.ckeys:
			self.tcombo = settings.dtcombo
	for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
		if key in kdowns:
			self.ckeys.add(key)
			self.tspan = self.tcombo
	if self.ckeys:
		self.tcombo += dt
		if self.tcombo >= settings.dtcombo:
			state.you.control(self.ckeys)
			self.tcombo = 0
			self.ckeys = set()
			if self.tspan > 0:
				learntspan(self.tspan)
	state.you.think(dt)
	view.think(dt)

def draw():
	pview.fill((40, 40, 120))
	for x in range(0, state.w + 1):
		p0 = view.worldtoscreen((x, 0))
		p1 = view.worldtoscreen((x, state.h))
		pygame.draw.line(pview.screen, (255, 0, 255), p0, p1, T(1))
	for y in range(0, state.h + 1):
		p0 = view.worldtoscreen((0, y))
		p1 = view.worldtoscreen((state.w, y))
		pygame.draw.line(pview.screen, (255, 0, 255), p0, p1, T(1))
	state.you.draw()
	for lep in state.leps:
		lep.draw()
	if self.alpha:
		pview.fill((255, 255, 255, int(255 * self.alpha)))


tspans = []
def learntspan(t):
	tspans.append(t)
	if settings.DEBUG and len(tspans) % 10 == 0:
		mu = statistics.mean(tspans)
		sigma = statistics.stdev(tspans)
		h = mu + 5 * sigma
		print("learntspan", len(tspans), max(tspans), mu, sigma, h,
			statistics.mean(tspan > h for tspan in tspans))

