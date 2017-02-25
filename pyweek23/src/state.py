from __future__ import division
import math, random, pygame, bisect
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
companion = True
basedamage = 1
reloadtime = 0.2
maxcharge = 9
chargetime = 3
vshots = 3
missiletime = 0.6
cshottime = 1
rmagnet = 200

tslow = 0
tinvulnerable = 0
tlose = 0
twin = 0

apickup = 0

scrollspeed = 40
xoffset = 0
yrange = 320

met = set()
saved = set()
good = False
best = False

def downgrade(name):  # or upgrade
	global hp0, hp, cshottime, companion, shieldhp0, shieldhp, missiletime, vshots, chargetime
	if name == "hp":
		hp0 -= 3
		hp = max(hp, hp0)
	if name == "cshot":
		cshottime = 1e12
	if name == "companion":
		companion = False
	if name == "shield":
		shieldhp0 = 0
		shieldhp = 0
	if name == "missile":
		missiletime = 1e12
	if name == "vshot":
		vshots = 0
	if name == "charge":
		chargetime = 1e12
	if name == "upgrade":
		hp = hp0 = 5
		cshottime = 1
		companion = True
		shieldhp = shieldhp0 = 2
		missiletime = 0.6
		vshots = 3
		chargetime = 3


yous = []
badbullets = []
goodbullets = []
pickups = []
enemies = []
bosses = []
planets = []
spawners = []
corpses = []
thinkers = yous, badbullets, goodbullets, pickups, enemies, bosses, planets, spawners, corpses
def clear():
	for group in thinkers:
		del group[:]
def restart():
	global twin, tlose, tslow, tinvulnerable, xoffset
	twin = tlose = tslow = tinvulnerable = xoffset = 0

def collided(obj1, obj2):
	return (obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2 < (obj1.r + obj2.r) ** 2

def getcollisions(A, B):
	if not B: return
	t0 = pygame.time.get_ticks()
	rmax = max(b.r for b in B)
	B = sorted(B, key = lambda b: b.x)
	xs = [b.x for b in B]
	for a in A:
		drmax = a.r + rmax
		j = bisect.bisect(xs, a.x - drmax)
		while j < len(B):
			b = B[j]
			dx, dy = b.x - a.x, b.y - a.y
			if dx > drmax:
				break
			dr = a.r + b.r
			if dx * dx + dy * dy < dr * dr:
				yield a, b
			j += 1

def think(dt):
	global xoffset, tslow, tinvulnerable, tlose, twin, shieldhp
	from . import scene, losescene
	tslow = max(tslow - dt, 0)
	if tslow > 0:
		dt /= min(3, 1 + 2 * tslow)
	tinvulnerable = max(tinvulnerable - dt, 0)
	shieldhp = min(shieldhp + shieldrate * dt, shieldhp0)
	xoffset += dt * scrollspeed
	for group in thinkers:
		for x in group:
			x.think(dt)
	for obj in planets:
		if collided(obj, you):
			obj.visit()
	for y, b in getcollisions(yous + planets, badbullets):
		b.hit(y)
	for b, e in getcollisions(goodbullets, enemies + bosses + planets):
		b.hit(e)
	for obj in enemies + bosses:
		if collided(obj, you):
			obj.hit(you)
	for obj in pickups:
		if collided(obj, you):
			obj.collect()
	for group in thinkers:
		group[:] = [x for x in group if x.alive]
	for wave in waves:
		if you.t >= wave[0]:
			func = wave[1]
			args = wave[2:]
			func(*args)
	waves[:] = [wave for wave in waves if you.t < wave[0]]
	if not you.alive:
		tlose += dt
		if tlose > 3:
			scene.pop()
			scene.push(losescene)
	elif not waves and not bosses and not spawners:
		twin += dt
		import thing
		for b in badbullets:
			corpses.append(thing.Corpse(x = b.x, y = b.y, r = b.r, lifetime = 1))
			b.alive = False
		if twin > 2:
			you.x += (twin - 2) * 1000 * dt
			if you.x > 1000:
				win()

def win():
	if stage == 1:
		gotostage(2)
	elif stage == 2:
		gotostage(3)
	elif stage == 3:
		met.add("7")
		met.add("C")
		met.add("J")
		gotostage(4)
	elif stage == 4:
		gotoclimax()
	else:
		raise ValueError("End of the game")

def gotostage(n):
	from . import playscene, scene
	scene.quit()
	scene.push(playscene, n)

def gotoclimax(n):
	from . import playscene, scene
	scene.quit()
	scene.push(playscene, n)

def draw():
	drawers = corpses, bosses, enemies, planets, yous, goodbullets, badbullets, pickups, spawners
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
	you.iflash = tinvulnerable
	if hp <= 0:
		you.die()

def heal(amount):
	global hp
	hp = min(hp + amount, hp0)

apickup0 = 30
def addapickup(amount, who):
	global apickup
	import thing
	old = apickup
	apickup += amount
	if old < apickup0 and apickup >= apickup0:
		spawnpickup(who, thing.HealthPickup)
	elif old < 2 * apickup0 and apickup >= 2 * apickup0:
		spawnpickup(who, thing.MissilesPickup)
	while apickup >= 2 * apickup0:
		apickup -= 2 * apickup0

def spawnpickup(who, ptype):
	x, y = who.x, who.y
	vx = 200
	vy = 50 if y < 0 else -50
	pickups.append(ptype(x = x, y = y, vx = vx, vy = vy, ax = -200))

def addmedusa():
	import thing
	boss = thing.Medusa(x = 600, y = 0, xtarget = 320)
	bosses.append(boss)
	for jtheta in (0, 1, 2):
		for jr, r in enumerate((20, 18, 16, 15, 14, 13, 12)):
			theta = (jtheta / 3 + jr / 40) * math.tau
			diedelay = 0.5 + 0.2 * jr
			snake = thing.Asp(target = boss, omega = -0.8, R = 100, theta = theta, r = r, diedelay = diedelay)
			enemies.append(snake)

			theta = (jtheta / 3 - jr / 70) * math.tau
			snake = thing.Asp(target = boss, omega = 0.5, R = 150, theta = theta, r = r, diedelay = diedelay)
			enemies.append(snake)

def addegret():
	import thing
	boss = thing.Egret(x = 600, y = 0, xtarget0 = 280)
	bosses.append(boss)

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

def addturkeywave(x0, y0, nx, ny, steps):
	import thing
	dxs, dys, dts = [], [], []
	r = 100
	for jx in range(nx):
		for jy in range(ny):
			dxs.append((jx - (nx - 1) / 2) * r)
			dys.append((jy - (ny - 1) / 2) * r)
			dts.append(math.phi * (len(dxs)) % 1)
	for dx, dy, dt in zip(dxs, dys, dts):
		esteps = [(t + dt, x + dx, y + dy) for t, x, y in steps]
		obj = thing.Turkey(x = x0 + dx, y = y0 + dy, steps = esteps)
		enemies.append(obj)

def addheronwave(n, dt):
	import thing
	vx = -20
	x0 = 600
	for j in range(n):
		y = ((j + 1) * math.phi % 1 * 2 - 1) * yrange
		obj = thing.Heron(x = x0 + j * abs(vx) * dt, y = y, vx = vx, vy = 0)
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

# I regret nothing.
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

