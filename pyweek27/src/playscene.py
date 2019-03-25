import random
from . import pview, thing, flake

class self:
	pass

def init():
	self.coins = [
	]
	def randomcircle():
		return (random.uniform(0, 1), random.uniform(0, 1)), random.uniform(0.2, 0.4) ** 2, random.choice(["red", "orange", "yellow", "white", "green"])
	self.flakes = [
		flake.Flake({
			"circles": [
				randomcircle() for _ in range(40)
			],
		}, (400, 300), 400)
	]
	
	self.pointed = None
	self.held = None

def think(dt, controls):
	self.pointed = None
	if not self.held:
		for coin in self.coins:
			if coin.collide(controls.mpos):
				self.pointed = coin
	if controls.mdown and self.pointed:
		self.held = self.pointed
		self.pointed = None
		self.coins.remove(self.held)
	if controls.mup and self.held:
		self.coins.append(self.held)
		self.held = None
	if self.held:
		self.held.pos = controls.mpos

def draw():
	pview.fill((80, 80, 200))
	if self.pointed is not None:
		self.pointed.highlight()
	for flake in self.flakes:
		flake.draw()
	for coin in self.coins:
		coin.draw()

	if self.held:
		self.held.draw()

