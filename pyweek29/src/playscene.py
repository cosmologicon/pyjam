import statistics
import pygame
from . import pview, view, thing, state, settings
from .pview import T

class self:
	pass

def init():
	state.you = thing.You()
	state.w = 10
	state.h = 10
	self.tcombo = 0
	self.ckeys = set()
	self.tspan = 0

def think(dt, kdowns):
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


tspans = []
def learntspan(t):
	tspans.append(t)
	if settings.DEBUG and len(tspans) % 10 == 0:
		mu = statistics.mean(tspans)
		sigma = statistics.stdev(tspans)
		h = mu + 5 * sigma
		print("learntspan", len(tspans), max(tspans), mu, sigma, h,
			statistics.mean(tspan > h for tspan in tspans))

