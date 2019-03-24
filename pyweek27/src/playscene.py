from . import pview, thing

class self:
	pass

def init():
	self.coins = [
		thing.Coin((100, 100), 6),
		thing.Coin((700, 200), 6),
		thing.Coin((500, 300), 6),
		thing.Coin((1000, 400), 6),
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
	for coin in self.coins:
		coin.draw()

	if self.held:
		self.held.draw()

