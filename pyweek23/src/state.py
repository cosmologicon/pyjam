
you = None
speed = 200
hp = 100

scrollspeed = 40
yrange = 320

yous = []
badbullets = []
goodbullets = []
pickups = []
enemies = []
planets = []

visited = set()

def collided(obj1, obj2):
	return (obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2 < (obj1.r + obj2.r) ** 2

def think(dt):
	thinkers = yous, badbullets, goodbullets, pickups, enemies, planets
	for group in thinkers:
		for x in group:
			x.think(dt)
	for obj in planets:
		if collided(obj, you):
			obj.visit()
	for obj in badbullets:
		for y in yous:
			if collided(obj, y):
				obj.hit(y)
		for planet in planets:
			if collided(obj, planet):
				obj.hit(planet)
	for group in thinkers:
		group[:] = [x for x in group if x.alive]

def draw():
	drawers = planets, enemies, yous, goodbullets, badbullets, pickups
	for group in drawers:
		for obj in group:
			obj.draw()

def takedamage(damage):
	global hp
	hp -= damage

