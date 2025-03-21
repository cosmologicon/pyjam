from __future__ import division
import math, random, pygame, bisect, os.path, os
from . import settings
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
miracle = False

tslow = 0
tinvulnerable = 0
dtinvulnerable = 1.5
tlose = 0
twin = 0
downgraded = False

apickup = 0

scrollspeed = 40
xoffset = 0
yrange = 320

met = set()
saved = set()
good = False
best = False

def downgrade(name):  # or upgrade
	global hp0, hp, cshottime, companion, shieldhp0, shieldhp, missiletime, vshots, chargetime, dtinvulnerable, downgraded
	if name == "hp":
		hp0 -= 3
		hp = max(hp, hp0)
		downgraded = True
	if name == "cshot":
		cshottime = 1e12
		downgraded = True
	if name == "companion":
		companion = False
		downgraded = True
	if name == "shield":
		shieldhp0 -= 1
		shieldhp = max(shieldhp, shieldhp0)
		downgraded = True
	if name == "missile":
		missiletime = 1e12
		downgraded = True
	if name == "vshot":
		vshots = 0
		downgraded = True
	if name == "charge":
		dtinvulnerable = 0.6
		downgraded = True
	if name == "upgrade":
		hp = hp0 = 5
		cshottime = 1
		companion = True
		shieldhp0 = 4 if miracle else 2
		shieldhp = shieldhp0
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
	global xoffset, tslow, tinvulnerable, tlose, twin
	global shieldhp, shieldhp0, miracle, apickup0, shieldrate
	from . import scene, losescene
	if settings.miracle and not miracle:
		miracle = True
		shieldhp += 2
		shieldhp0 += 2
		apickup0 /= 2
		shieldrate *= 2
	elif miracle and not settings.miracle:
		miracle = False
		shieldhp -= 2
		shieldhp0 -= 2
		apickup0 *= 2
		shieldrate /= 2
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
			removequicksave()
	elif not waves and not bosses and not spawners:
		twin += dt
		from . import thing
		for b in badbullets:
			corpses.append(thing.Corpse(x = b.x, y = b.y, r = b.r, lifetime = 1))
			b.alive = False
		if twin > 2:
			you.x += (twin - 2) * 1000 * dt
			if you.x > 1000:
				win()

def win():
	from . import scene, winscene
	if stage == 1:
		gotostage(2)
		save(settings.progressfile)
		removequicksave()
	elif stage == 2:
		gotostage(3)
		save(settings.progressfile)
		removequicksave()
	elif stage == 3:
		met.add("C")
		met.add("J")
		gotostage(4)
		save(settings.progressfile)
		removequicksave()
	elif stage == 4:
		if all(s in saved for s in "123456X"):
			gotoclimax()
		else:
			scene.quit()
			scene.push(winscene)
	else:
		raise ValueError("End of the game")

def gotostage(n):
	from . import playscene, scene
	scene.quit()
	scene.push(playscene, n)

def gotoclimax():
	from . import climaxscene, scene
	scene.quit()
	scene.push(climaxscene)

def draw():
	drawers = corpses, bosses, enemies, planets, yous, goodbullets, badbullets, pickups, spawners
	for group in drawers:
		for obj in group:
			obj.draw()

def takedamage(damage):
	global hp, tinvulnerable, shieldhp
	from . import sound
	if tinvulnerable:
		return
	while shieldhp >= 1 and damage:
		shieldhp -= 1
		damage -= 1
	hp -= damage
	tinvulnerable = dtinvulnerable
	you.iflash = tinvulnerable
	if hp <= 0:
		you.die()
		sound.playsfx("you-die")
	else:
		sound.playsfx("you-hurt")
		

def heal(amount):
	global hp
	hp = min(hp + amount, hp0)

apickup0 = 30
def addapickup(amount, who):
	global apickup
	from . import thing
	old = apickup
	apickup += amount
	if old < apickup0 and apickup >= apickup0:
		spawnpickup(who, thing.HealthPickup)
	elif old < 2 * apickup0 and apickup >= 2 * apickup0:
		spawnpickup(who, thing.HealthPickup)
	while apickup >= 2 * apickup0:
		apickup -= 2 * apickup0

def spawnpickup(who, ptype):
	x, y = who.x, who.y
	vx = 200
	vy = 50 if y < 0 else -50
	pickups.append(ptype(x = x, y = y, vx = vx, vy = vy, ax = -200))

def addmedusa():
	from . import thing
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
	from . import thing
	boss = thing.Egret(x = 600, y = 0, xtarget0 = 280)
	bosses.append(boss)

def addduckwave(x0, y0, nx, ny, steps):
	from . import thing
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
	from . import thing
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
	from . import thing
	vx = -20
	x0 = 600
	for j in range(n):
		y = ((j + 1) * math.phi % 1 * 2 - 1) * yrange
		obj = thing.Heron(x = x0 + j * abs(vx) * dt, y = y, vx = vx, vy = 0)
		enemies.append(obj)

def addrockwave(x0, y0, n, spread):
	from . import thing
	for j in range(n):
		x = random.gauss(x0, 0.4 * spread)
		y = random.gauss(y0, spread)
		vx = random.uniform(-100, -40)
		r = random.uniform(30, random.uniform(30, 50))
		rock = thing.Rock(x = x, y = y, vx = vx, vy = 0, r = r, hp = 20)
		enemies.append(rock)

# I regret nothing.
obj0 = pickle.dumps([(k, v) for k, v in globals().items() if not k.startswith("_") and type(v) not in [type(pickle), type(think)]], 2)
def reset():
	g = globals()
	for k, v in pickle.loads(obj0):
		g[k] = v

def save(filename):
	if not os.path.exists(settings.savedir):
		os.makedirs(settings.savedir)
	path = os.path.join(settings.savedir, filename)
	obj = [(k, v) for k, v in globals().items() if not k.startswith("_") and type(v) not in [type(pickle), type(think)]]
	pickle.dump(obj, open(path, "wb"), 2)

def getmsave():
	mfile = os.path.join(settings.savedir, settings.miraclefile)
	if os.path.exists(mfile):
		return pickle.load(open(mfile, "rb"))
	return set(), set()

def mupdate():
	if not os.path.exists(settings.savedir):
		os.makedirs(settings.savedir)
	msaved, mmet = getmsave()
	mfile = os.path.join(settings.savedir, settings.miraclefile)
	msaved |= saved
	mmet |= met
	pickle.dump((msaved, mmet), open(mfile, "wb"), 2)

def removequicksave():
	qfile = os.path.join(settings.savedir, settings.quicksavefile)
	if os.path.exists(qfile):
		os.remove(qfile)

def load(filename):
	obj = pickle.load(open(filename, "rb"))
	g = globals()
	for k, v in obj:
		g[k] = v

def startup():
	global saved, met
	from . import scene, playscene, losescene
	if settings.restart:
		removequicksave()
		deleteprogress()
	qfile = os.path.join(settings.savedir, settings.quicksavefile)
	if os.path.exists(qfile):
		load(qfile)
		scene.push(playscene, stage)
		load(qfile)
		return
	pfile = os.path.join(settings.savedir, settings.progressfile)
	if os.path.exists(pfile):
		scene.push(losescene)
		return
	if settings.miracle:
		msaved, mmet = getmsave()
		saved |= msaved
		met |= mmet
	scene.push(playscene, 1)

def loadandrun():
	global saved, met
	from . import scene, playscene
	scene.quit()
	pfile = os.path.join(settings.savedir, settings.progressfile)
	if os.path.exists(pfile):
		load(pfile)
		scene.push(playscene, stage)
	else:
		reset()
		if settings.miracle:
			msaved, mmet = getmsave()
			saved |= msaved
			met |= mmet
		scene.push(playscene, 1)

def deleteprogress():
	pfile = os.path.join(settings.savedir, settings.progressfile)
	if os.path.exists(pfile):
		os.remove(pfile)
		


