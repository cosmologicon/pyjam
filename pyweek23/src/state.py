from __future__ import division
import math, random
try:
    import cPickle as pickle
except ImportError:
    import pickle


you = None
speed = 200
hp0 = 5
hp = hp0
shieldhp = shieldhp0 = 2
shieldrate = 0.2


basedamage = 1
reloadtime = 0.2
maxcharge = 9
chargetime = 3
vshots = 2
missiletime = 0.6
cshottime = 1
rmagnet = 200
tslow = 0
tinvulnerable = 0
tlose = 0

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
spawners = []

visited = set()

def collided(obj1, obj2):
	return (obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2 < (obj1.r + obj2.r) ** 2

def think(dt):
	global xoffset, tslow, tinvulnerable, tlose, shieldhp
	from . import scene, losescene
	tslow = max(tslow - dt, 0)
	if tslow > 0:
		dt /= min(3, 1 + 2 * tslow)
	tinvulnerable = max(tinvulnerable - dt, 0)
	shieldhp = min(shieldhp + shieldrate * dt, shieldhp0)
	xoffset += dt * scrollspeed
	thinkers = yous, badbullets, goodbullets, pickups, enemies, bosses, planets, spawners
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
	for obj in enemies + bosses:
		if collided(obj, you):
			obj.hit(you)
	for obj in pickups:
		if collided(obj, you):
			obj.collect()
	for group in thinkers:
		group[:] = [x for x in group if x.alive]
	while waves and you.t > waves[0][0]:
		wave = waves[0]
		del waves[0]
		func = wave[1]
		args = wave[2:]
		func(*args)
	if not you.alive:
		tlose += dt
		if tlose > 3:
			scene.pop()
			scene.push(losescene)


def draw():
	drawers = planets, bosses, enemies, yous, goodbullets, badbullets, pickups
	for group in drawers:
		for obj in group:
			obj.draw()

def takedamage(damage):
	global hp, tinvulnerable, shieldhp
	if tinvulnerable:
		return
	while shieldhp >= 1 and damage:
		shieldhp -= 1
		damage -= 1
	hp -= damage
	tinvulnerable = 1
	if hp <= 0:
		you.die()

def heal(amount):
	global hp
	hp = min(hp + amount, hp0)

def addmedusa():
	import thing
	boss = thing.Medusa(x = 600, y = 0, xtarget = 320)
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

def addduckwave(x0, y0, nx, ny, steps):
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

def addrockwave(x0, y0, n, spread):
	import thing
	for j in range(n):
		x = random.gauss(x0, 0.4 * spread)
		y = random.gauss(y0, spread)
		vx = random.uniform(-100, -40)
		r = random.uniform(30, random.uniform(30, 50))
		rock = thing.Rock(x = x, y = y, vx = vx, vy = 0, r = r, hp = 20)
		enemies.append(rock)

obj0 = pickle.dumps([(k, v) for k, v in globals().items() if not k.startswith("_") and type(v) is not type(pickle)], 2)
def reset():
	g = globals()
	for k, v in pickle.loads(obj0):
		g[k] = v

def save(filename):
	obj = [(k, v) for k, v in globals().items() if not k.startswith("_") and type(v) is not type(pickle)]
	pickle.dump(obj, open(filename, "wb"), 2)

def load(filename):
	obj = pickle.load(open(filename, "rb"))
	g = globals()
	for k, v in obj:
		g[k] = v

