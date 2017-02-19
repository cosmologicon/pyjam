
you = None
speed = 500

scrollspeed = 40
yrange = 320

badbullets = []
enemies = []

def think(dt):
	you.think(dt)
	thinkers = badbullets, enemies
	for group in thinkers:
		for x in group:
			x.think(dt)
	for group in (badbullets, enemies):
		group[:] = [x for x in group if x.alive]

def draw():
	you.draw()
	drawers = enemies, badbullets
	for group in drawers:
		for obj in group:
			obj.draw()


