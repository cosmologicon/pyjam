# Frame-by-frame game state. Can be reset without loss of progress.

try:
	import cPickle as pickle
except ImportError:
	import pickle
import os, os.path, math, random
from . import util, progress, settings, level, ptext

drawables = []
colliders = []
mouseables = []
thinkers = []
buildables = []
shootables = []

groups = drawables, colliders, mouseables, thinkers, buildables, shootables

def reset(lname):
	from .import thing
	global levelname, tlevel, wavespecs, donewaves, atp, cell, health, Rlevel, twin, tlose
	levelname = lname
	tlevel = 0
	twin = tlose = 0
	leveldata = level.data[levelname]
	for group in groups:
		del group[:]

	wavespecs = leveldata["wavespecs"]
	donewaves = []
	atp = leveldata.get("atp", [0, 0])
	pos = leveldata["cellpos"]
	cell = thing.Amoeba(x = pos[0], y = pos[1])
	cell.addtostate()
	Rlevel = leveldata["Rlevel"]
	health = leveldata["health"]

def setgroups(obj):
	for x, y in zip(obj, groups):
		y[:] = x

def updatealive():
	for group in groups:
		group[:] = [m for m in group if m.alive]

def think(dt):
	global tlevel, twin, tlose
	tlevel += dt
	for wave in wavespecs:
		if wave[0] < tlevel:
			launchwave(wave)
	updatealive()
	if complete():
		twin += dt
	if not cell.alive:
		tlose += dt

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
	twave, angle, nant = wave
	for jant in range(nant):
		theta = angle + random.uniform(-0.05, 0.05)
		step = random.uniform(30, 60)
		x, y = outstep(theta, step)
		ant = thing.Ant(x = x, y = y)
		ant.target = cell
		ant.addtostate()
	if levelname == "endless":
		addendlesswave()

def addendlesswave():
	jwave = len(donewaves)
	tlast, anglelast, nantlast = donewaves[-1]
	t = tlast + 20
	angle = (anglelast + (math.sqrt(5) + 1) / 2) % 1
	wavespecs.append((t, angle, nantlast))

def drawwaves():
	from . import view
	for wave in wavespecs + donewaves:
		t, angle, nant = wave
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
		fontsize = view.screenlength(20)
		x, y = outstep(angle, 20)
		x += 0.2 * (cell.x - x)
		y += 0.2 * (cell.y - y)
		ptext.draw(text, midtop = view.screenpos((x, y)), angle = -360 * angle,
			fontsize = fontsize, fontname = "Stint", lineheight = 0.85,
			color = "#FF4F4F", shadow = (0.5, 1), alpha = 0.4 * alpha)

def complete():
	return not shootables and not wavespecs

def removeobj(obj):
	temp = obj.alive
	obj.alive = False
	updatealive()
	obj.alive = temp

def save():
	obj = progress.getprogress(), groups, levelname, atp, cell, health, Rlevel, wavespecs, donewaves, twin, tlose
	filename = settings.statepath
	util.mkdir(filename)
	pickle.dump(obj, open(filename, "wb"))

def canload():
	filename = settings.statepath
	return os.path.exists(filename)

def load():
	global levelname, atp, cell, health, Rlevel, wavespecs, donewaves, twin, tlose
	filename = settings.statepath
	obj = pickle.load(open(filename, "rb"))
	pstate, gstate, levelname, atp, cell, health, Rlevel, wavespecs, donewaves, twin, tlose = obj
	progress.setprogress(pstate)
	setgroups(gstate)

def removesave():
	filename = settings.statepath
	if os.path.exists(filename):
		os.remove(filename)


