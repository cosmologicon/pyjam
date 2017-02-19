
you = None
speed = 500

scrollspeed = 40
yrange = 320

badbullets = []
goodbullets = []
pickups = []
enemies = []
planets = []

visited = set()

def collided(obj1, obj2):
	return (obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2 < (obj1.r + obj2.r) ** 2

def think(dt):
	thinkers = [you], badbullets, goodbullets, pickups, enemies, planets
	for group in thinkers:
		for x in group:
			x.think(dt)
	for group in thinkers:
		group[:] = [x for x in group if x.alive]
	for obj in planets:
		if collided(obj, you):
			obj.visit()
	for obj in badbullets:
		if collided(obj, you):
			obj.hit()

def draw():
	drawers = planets, enemies, [you], goodbullets, badbullets, pickups
	for group in drawers:
		for obj in group:
			obj.draw()


