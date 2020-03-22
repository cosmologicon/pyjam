import pygame
from . import settings

# A combo is completed if any of the following happen:
# 1. a non-combo key is pressed.
# 2. any key is released.
# 3. a length of time (settings.dtcombo) has passed since the combo began

class self:
	pass

def init():
	self.queue = []  # completed events
	self.tcombo = 0  # time since current combo began
	self.ckeys = set()  # current combo in progress


def think(dt):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			for key, keycodes in settings.keys.items():
				if event.key in keycodes:
					keydown(key)
		if event.type == pygame.KEYUP:
			for key, keycodes in settings.keys.items():
				if event.key in keycodes:
					keyup(key)
	if self.ckeys:
		self.tcombo += dt
		if self.tcombo >= settings.dtcombo:
			self.completecombo()

combokeys = "up", "down", "left", "right"

def completecombo():
	self.queue.append(("combo",) + tuple(self.ckeys))
	self.ckeys = set()
	self.tcombo = 0

def keydown(key):
	if key in combokeys:
		if not self.ckeys:
			self.tcombo = 0
		self.ckeys.add(key)
	else:
		if self.ckeys:
			completecombo()
		self.queue.append((key,))

def keyup(key):
	completecombo()

def get():
	yield from self.queue
	self.queue = []



tspans = []
def learntspan(t):
	tspans.append(t)
	if settings.DEBUG and len(tspans) % 10 == 0:
		mu = statistics.mean(tspans)
		sigma = statistics.stdev(tspans)
		h = mu + 5 * sigma
		print("learntspan", len(tspans), max(tspans), mu, sigma, h,
			statistics.mean(tspan > h for tspan in tspans))

