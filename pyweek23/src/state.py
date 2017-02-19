from __future__ import division
import math



you = None
speed = 200
hp0 = 100
hp = 100
basedamage = 1
reloadtime = 0.2
maxcharge = 9
chargetime = 3
missiletime = 0.6

scrollspeed = 40
xoffset = 0
yrange = 320

yous = []
badbullets = []
goodbullets = []
pickups = []
enemies = []
planets = []
bosses = []

visited = set()

def collided(obj1, obj2):
	return (obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2 < (obj1.r + obj2.r) ** 2

def think(dt):
	global xoffset
	xoffset += dt * scrollspeed
	thinkers = yous, badbullets, goodbullets, pickups, enemies, bosses, planets
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
	for obj in goodbullets:
		for e in enemies + bosses:
			if collided(obj, e):
				obj.hit(e)
		for planet in planets:
			if collided(obj, planet):
				obj.hit(planet)
	for group in thinkers:
		group[:] = [x for x in group if x.alive]

def draw():
	drawers = planets, bosses, enemies, yous, goodbullets, badbullets, pickups
	for group in drawers:
		for obj in group:
			obj.draw()

def takedamage(damage):
	global hp
	hp -= damage

def addmedusa(x, y):
	import thing
	boss = thing.Medusa(x = x, y = y, vx = -5)
	bosses.append(boss)
	for jtheta in (0, 1, 2):
		for jr, r in enumerate((20, 18, 16, 15, 14, 13, 12)):
			theta0 = (jtheta / 3 + jr / 40) * math.tau
			diedelay = 0.5 + 0.2 * jr
			snake = thing.SnakeSegment(target = boss, omega = -0.8, R = 100, theta0 = theta0, r = r, diedelay = diedelay)
			enemies.append(snake)

			theta0 = (jtheta / 3 - jr / 70) * math.tau
			snake = thing.SnakeSegment(target = boss, omega = 0.5, R = 150, theta0 = theta0, r = r, diedelay = diedelay)
			enemies.append(snake)

def addwave(x0, y0, nx, ny, steps):
	import thing
	dxs, dys, dts = [], [], []
	r = 50
	for jx in range(nx):
		for jy in range(ny):
			dxs.append((jx - (nx - 1) / 2) * r)
			dys.append((jy - (ny - 1) / 2) * r)
			dts.append(math.phi * (len(dxs)) % 1)
	for dx, dy, dt in zip(dxs, dys, dts):
		esteps = [(t + dt, x + dx, y + dy) for t, x, y in steps]
		obj = thing.Duck(x = x0 + dx, y = y0 + dy, steps = esteps)
		enemies.append(obj)




