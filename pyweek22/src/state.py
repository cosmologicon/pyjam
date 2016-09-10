# Frame-by-frame game state. Can be reset without loss of progress.

from __future__ import division
try:
	import cPickle as pickle
except ImportError:
	import pickle
import os, os.path, math, random
from . import util, progress, settings, level, ptext, mechanics, dialog, sound

drawables = []
colliders = []
mouseables = []
thinkers = []
buildables = []
shootables = []
bosses = []

groups = drawables, colliders, mouseables, thinkers, buildables, shootables, bosses

def reset(lname):
	from .import thing
	global levelname, tlevel, wavespecs, donewaves, atp, cell, health, Rlevel, twin, tlose
	levelname = lname
	tlevel = 0
	twin = tlose = 0
	leveldata = level.data[levelname]
	for group in groups:
		del group[:]

	wavespecs = list(leveldata["wavespecs"])
	donewaves = []
	atp = list(leveldata.get("atp", [0, 0]))
	pos = leveldata["cellpos"]
	cell = thing.Amoeba(x = pos[0], y = pos[1], nslot = progress.nslots)
	cell.addtostate()
	Rlevel = leveldata["Rlevel"]
	health = leveldata["health"]
	if settings.quickstart:
		atp = [10000, 10000]
	
	if levelname == 3:
		thing.Wasp(x = 0, y = 150).addtostate()

	if levelname == 6:
		for j in range(3):
			w = thing.Hornet(x = 0, y = 150)
			w.addtostate()
			w.theta = j * math.tau / 3
			w.think(random.random())

	if levelname == 9:
		for j in range(5):
			w = thing.Cricket(x = 0, y = 150)
			w.addtostate()
			w.theta = j * math.tau / 5
			w.think(random.random())

def setgroups(obj):
	for x, y in zip(obj, groups):
		y[:] = x

def updatealive():
	for group in groups:
		group[:] = [m for m in group if m.alive]

def think(dt):
	global tlevel, twin, tlose, health
	from . import thing
	if dialog.quiet():
		if any(tlevel <= wave[0] - n < tlevel + dt for n in (0, 1, 2) for wave in wavespecs):
			sound.playsfx("tick")
		tlevel += dt
	for wave in wavespecs:
		if wave[0] < tlevel:
			launchwave(wave)
	for t, etype, n0, dn in level.data[levelname].get("streamspecs", []):
		t = tlevel - t
		if t > 0:
			n = (n0 + dn * t) / 100
			if random.random() < n * dt:
				stream(etype)

	updatealive()
	if complete():
		twin += dt
	if tlose or health <= 0:
		tlose += dt
	health = min(health + cell.countflavors(2) * dt, level.data[levelname]["health"])
	autoatp = level.data[levelname].get("autoatp", (0, 0))
	if random.random() < autoatp[0] * dt:
		x, y = randomatppos()
		thing.ATP1(x = x, y = y).addtostate()
	if random.random() < autoatp[1] * dt:
		x, y = randomatppos()
		thing.ATP2(x = x, y = y).addtostate()

def randomatppos():
	x = random.uniform(-Rlevel, Rlevel)
	y = random.uniform(-Rlevel, Rlevel)
	if x ** 2 + y ** 2 > Rlevel ** 2:
		return randomatppos()
	if cell.distanceto((x, y)) < 2 * cell.rcollide:
		return randomatppos()
	return x, y

def takedamage(damage):
	global health
	for j in range(cell.countflavors(0)):
		damage *= 0.7
	health -= damage

def outstep(theta, step):
	theta *= math.tau
	dx, dy = step * math.sin(theta), step * math.cos(theta)
	x, y = cell.x, cell.y
	while x ** 2 + y ** 2 < (Rlevel + 10) ** 2:
		x += dx
		y += dy
	return x, y

def launchwave(wave):
	from . import thing
	donewaves.append(wave)
	wavespecs.remove(wave)
	twave, angle, etype, n = wave
	for jant in range(n):
		theta = angle + random.uniform(-0.05, 0.05)
		step = random.uniform(30, 60)
		x, y = outstep(theta, step)
		addetype(etype, x, y)
	if levelname == "endless":
		addendlesswave()

def stream(etype):
	from . import thing
	theta = random.angle()
	step = random.uniform(30, 60)
	x, y = outstep(theta, step)
	addetype(etype, x, y)

def addetype(etype, x, y):
	from . import thing
	if etype == "ant":
		ant = thing.Ant(x = x, y = y)
		ant.target = cell
		ant.addtostate()
	if etype == "Lant":
		ant = thing.LargeAnt(x = x, y = y)
		ant.target = cell
		ant.addtostate()
	if etype == "bee":
		bee = thing.Bee(x = x, y = y)
		bee.target = cell
		bee.addtostate()
	if etype == "Lbee":
		bee = thing.LargeBee(x = x, y = y)
		bee.target = cell
		bee.addtostate()
	if etype == "flea":
		flea = thing.Flea(x = x, y = y)
		flea.target = cell
		flea.addtostate()

def addendlesswave():
	jwave = len(donewaves)
	tlast, anglelast, nantlast = donewaves[-1]
	t = tlast + 20
	angle = (anglelast + (math.sqrt(5) + 1) / 2) % 1
	wavespecs.append((t, angle, nantlast))

def drawwaves():
	from . import view
	drawn = set()
	for wave in wavespecs + donewaves:
		t, angle, etype, n = wave
		t = tlevel - t
		if t < -10:
			continue
		elif t < 0:
			text = "Wave\nincoming\nin:\n%d sec" % int(-t)
			alpha = math.clamp(t + 10, 0, 1)
		elif t < 10:
			text = "Wave\nincoming"
			alpha = math.clamp(10 - t, 0, 1)
		else:
			continue
		if angle in drawn:
			continue
		drawn.add(angle)
		fontsize = view.screenlength(20)
		x, y = outstep(angle, 20)
		x += 0.2 * (cell.x - x)
		y += 0.2 * (cell.y - y)
		ptext.draw(text, midtop = view.screenpos((x, y)), angle = -360 * angle,
			fontsize = fontsize, fontname = "Stint", lineheight = 0.85,
			color = "#FF4F4F", shadow = (0.5, 1), alpha = 0.4 * alpha)

def complete():
	if levelname in (3, 6, 9):
		return not bosses
	return not shootables and not wavespecs

def win():
	for obj in shootables:
		obj.die()
	del wavespecs[:]

def lose():
	global tlose
	tlose = 1000

def cheat():
	global health, atp
	health += 1000
	atp[0] += 1000
	atp[1] += 1000

def canbuy(flavor):
	(atp1, atp2) = {
		"X": (mechanics.Xcost1, mechanics.Xcost2),
		"Y": (mechanics.Ycost1, mechanics.Ycost2),
		"Z": (mechanics.Zcost1, mechanics.Zcost2),
	}[flavor]
	return atp[0] >= atp1 and atp[1] >= atp2

def buy(flavor):
	global atp
	(atp1, atp2) = {
		"X": (mechanics.Xcost1, mechanics.Xcost2),
		"Y": (mechanics.Ycost1, mechanics.Ycost2),
		"Z": (mechanics.Zcost1, mechanics.Zcost2),
	}[flavor]
	atp = [atp[0] - atp1, atp[1] - atp2]

def removeobj(obj):
	temp = obj.alive
	obj.alive = False
	updatealive()
	obj.alive = temp

def save():
	obj = progress.getprogress(), groups, levelname, atp, cell, health, Rlevel, wavespecs, donewaves, twin, tlose, tlevel
	filename = settings.statepath
	util.mkdir(filename)
	pickle.dump(obj, open(filename, "wb"))

def canload():
	filename = settings.statepath
	return os.path.exists(filename)

def load():
	global levelname, atp, cell, health, Rlevel, wavespecs, donewaves, twin, tlose, tlevel
	filename = settings.statepath
	obj = pickle.load(open(filename, "rb"))
	pstate, gstate, levelname, atp, cell, health, Rlevel, wavespecs, donewaves, twin, tlose, tlevel = obj
	progress.setprogress(pstate)
	setgroups(gstate)

def removesave():
	filename = settings.statepath
	if os.path.exists(filename):
		os.remove(filename)


