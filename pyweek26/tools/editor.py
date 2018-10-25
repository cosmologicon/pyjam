"""
A joiner consists of a series of sections joining two pools.

There are three types of sections within a joiner: straight, curved, and sloped.

The joiner must begin and end with a straight section, and there must be a straight section between
any two non-straight sections. For instance, one possible sequence is:

  pool - straight - curved - straight - sloped - straight - pool

Curved sections let you change the x-y orientation. Sloped sections let you change the z position.

Every joiner has a series of waypoints.
Sequences of sections are automatically generated using the joiner's waypoints.
There's an implicit waypoint at the pools on either end of the joiner.
If consecutive waypoints are on the same z-level they may be connected with just straight and curved.
Consecutive waypoints with different z-values require an intermediate sloped section.

PS this entire program is a nightmare.
"""

from __future__ import division
import sys, pygame, math, json, os, sys, random
from pygame.locals import *
from pygame.math import Vector2, Vector3
from . import ptext

savefile = "/tmp/flow.json"
dumpfile = "/tmp/leveldata.csv"

zoom = 1
p0 = Vector3(0, 0, 0)

# ISO convention https://en.wikipedia.org/wiki/Spherical_coordinate_system
theta = 1
phi = 0

w, h = 1024, 720
screen = pygame.display.set_mode((w, h))

# previous value  within sorted list vs less than v
def pvalue(vs, v, wrap=True):
	xs = [x for x in vs if x < v]
	return xs[-1] if xs else vs[-1 if wrap else 0]
# next value within sorted list vs greater than v
def nvalue(vs, v, wrap=True):
	xs = [x for x in vs if x > v]
	return xs[0] if xs else vs[0 if wrap else -1]

# Closest point to p on line joining p0 and p1
def xysnap(p0, p1, p):
	p0 = Vector2(*p0)
	p1 = Vector2(*p1)
	p = Vector2(*p)
	f = (p1 - p0).normalize()
	p = p0 + f * (p - p0).dot(f)
	return p.x, p.y

def screenpos(pos):
	p = (pos - p0).rotate_z(math.degrees(phi)).rotate_x(math.degrees(-theta)) * zoom
	return (
		int(w / 2 + p.x),
		int(h / 2 - p.y),
	)
def near(p, spos):
	return (Vector2(*screenpos(p)) - Vector2(spos)).length() < 10

def drawpoint(pos, r, color):
	r = max(1, int(round(r * zoom)))
	pygame.draw.circle(screen, color, screenpos(pos), r)
def drawellipse(pos, r, color):
	w = max(2, int(round(2 * r * zoom)))
	h = max(2, int(round(2 * r * zoom * math.cos(theta))))
	rect = pygame.Rect((0, 0, w, h))
	rect.center = screenpos(pos)
	pygame.draw.ellipse(screen, color, rect, 1)
def drawline(p0, p1, color):
	pygame.draw.line(screen, color, screenpos(p0), screenpos(p1))
def drawwideline(p0, p1, w, color):
	f = (p0 - p1).cross(Vector3(0, 0, 1))
	f = f.normalize() if f.length() else Vector3(1, 0, 0)
	for d in (-w, 0, w):
		drawline(p0 + d * f, p1 + d * f, color)

rpools = 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 17, 20, 22, 25, 27, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100
pressures = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
pools = [
]
rways = 0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 17, 20, 22, 25, 27, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100
joiners = [
]
pipes = [
]

def save():
	obj = { "pools": pools, "joiners": joiners, "pipes": pipes }
	json.dump(obj, open(savefile, "w"))
def load():
	global pools, joiners, pipes
	if not os.path.exists(savefile):
		return
	obj = json.load(open(savefile, "r"))
	pools = obj["pools"]
	joiners = obj["joiners"]
	pipes = obj["pipes"]
if not "--reset" in sys.argv:
	load()

def totuple(*args):
	return tuple(args)

def pipedata(jpipe, pipe):
	jp0 = pipe["jp0"]
	jp1 = pipe["jp1"]
	r = 1.5
	R = pools[jp0]["r"] + 2
	p0 = Vector3(*pools[jp0]["pos"]) + Vector3(0, 0, 0.8 * r)
	d = Vector3(*pools[jp1]["pos"]) - p0
	d.z = 0
	d = R * d.normalize()
	p1 = p0 + d
	return totuple("pipe", jpipe, "pool", jp0, "pool", jp1, *p0, *p1, r)

def extractjoiner(jjoiner, joiner):
	jp0 = joiner["jp0"]
	jp1 = joiner["jp1"]
	p0 = pools[jp0]["pos"]
	p1 = pools[jp1]["pos"]
	w = joiner["w"]
	waypoints = list(joiner["waypoints"])
	jcurves = [True] + [r > 0 for p, r in waypoints] + [True]
	p0s = [p0] + [p for p, r in waypoints] + [p1]
	ps = [p0]
	curvedata = []
	iscurve = [False]
	for k, (p, r) in enumerate(waypoints):
		if r == 0:
			ps.append(p)
			iscurve.append(False)
		else:
			k0, k1, k2 = k, k + 1, k + 2
			while not jcurves[k0]: k0 -= 1
			while not jcurves[k2]: k2 += 1
			pA, pB, pC = Vector3(p0s[k0]), Vector3(p0s[k1]), Vector3(p0s[k2])
			f0 = pB - pA
			f1 = pC - pB
			f0.z = 0
			f1.z = 0
			if f0.length() == 0 or f1.length == 0:
				print("Error dumping joiner %d: %s" % (jjoiner, joiner))
				return
			f0 = f0.normalize()
			f1 = f1.normalize()
			if abs(f0.dot(f1)) > 0.999:
				print("Error dumping joiner %d: %s" % (jjoiner, joiner))
				return
			f = (f1 - f0).normalize()
			z = f1.cross(f0).normalize()
			beta = 1/2 * math.acos(f0.dot(f1))
			center = pB + f * r / math.cos(beta)
			ps.append(center - r * f.rotate(math.degrees(beta), z))
			ps.append(center - r * f.rotate(math.degrees(-beta), z))
			curvedata.append((center, beta, z.z > 0))
			iscurve.append(True)
			iscurve.append(False)
	ps.append(p1)
	cons = [("pool", jp0)] + [(jjoiner, k) for k in range(len(ps) - 1)] + [("pool", jp1)]

	k = 0
	while len(ps) > 2:
		if ps[0][2] != ps[1][2]:
			yield totuple("slope", jjoiner, k, *cons[k], *cons[k+2], *ps[0], *ps[1], w)
		elif iscurve[k]:
			center, beta, right = curvedata[0]
			del curvedata[0]
			yield totuple("curve", jjoiner, k, *cons[k], *cons[k+2], *ps[0], *ps[1], w, *center, beta, right, r)
			k += 1
			del ps[0]
			yield totuple("straight", jjoiner, k, *cons[k], *cons[k+2], *ps[0], *ps[1], w)
		else:
			yield totuple("straight", jjoiner, k, *cons[k], *cons[k+2], *ps[0], *ps[1], w)
		del ps[0]
		k += 1
#		del waypoints[0]
	if len(ps) > 1:
		yield totuple("straight", jjoiner, k, *cons[k], *cons[k+2], *ps[0], *ps[1], w)

def dump():
	with open(dumpfile, "w") as f:
		def write(*args):
			f.write("\t".join(map(str, args)) + "\n")
		for jpool, pool in enumerate(pools):
			write("pool", jpool, *pool["pos"], pool["r"], pool["pressure"], pool["drainable"])
		for jpipe, pipe in enumerate(pipes):
			write(*pipedata(jpipe, pipe))
		for jjoiner, joiner in enumerate(joiners):
			for args in extractjoiner(jjoiner, joiner):
				write(*args)

cpools = []  # Currently selected pool indices, if any
cway = []   # Currently selected waypoint indices, if any
cjoin = None  # Currently selected join, if any

clock = pygame.time.Clock()
playing = True
while playing:
	dt = 0.001 * clock.tick(60)
	kdowns = set()
	kpressed = pygame.key.get_pressed()
	dmx, dmy = 0, 0
	mlclick = False
	mcenter = False
	mright = False
	scroll = 0
	for event in pygame.event.get():
		if event.type == QUIT:
			playing = False
		if event.type == KEYDOWN:
			kdowns.add(event.key)
		if event.type == MOUSEMOTION:
			dmx, dmy = event.rel
			mcenter = event.buttons[1]
			mright = event.buttons[2]
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				mlclick = event.pos
			scroll += event.button == 4
			scroll -= event.button == 5
	if K_ESCAPE in kdowns:
		playing = False
	if mlclick:
		topool = [jpool for jpool, pool in enumerate(pools) if near(Vector3(pool["pos"]), mlclick)]
		toway = [(j, k)
			for j, joiner in enumerate(joiners)
			for k, (waypoint, r) in enumerate(joiner["waypoints"])
			if near(waypoint, mlclick)
		]
		if kpressed[K_LSHIFT]:
			toadd = set(topool) - set(cpools)
			cpools = sorted((set(cpools) - set(topool)) | toadd)
			toadd = set(toway) - set(cway)
			cway = sorted((set(cway) - set(toway)) | toadd)
		else:
			if len(topool) == 1 and not cway and topool == cpools:
				cpools = []
			elif len(toway) == 1 and not cpools and toway == cway:
				cway = []
			else:
				cpools = topool
				cway = toway
		cjoin = None
	if K_SPACE in kdowns:
		if cpools:
			cpools = [(min(cpools) + 1) % len(pools)]
		elif pools:
			cpools = [0]
	if K_TAB in kdowns and len(cpools) == 1:
		pool = cpools[0]
		values = [None] + [jjoin for jjoin, join in enumerate(joiners) if pool in (join["jp0"], join["jp1"])]
		cjoin = values[(values.index(cjoin) + 1) % len(values) if cjoin in values else 0]
	scoot = 1 if kpressed[K_LSHIFT] else 10
	vscoot = Vector3([
		scoot * ((K_RIGHT in kdowns) - (K_LEFT in kdowns)),
		scoot * ((K_UP in kdowns) - (K_DOWN in kdowns)),
		scoot * ((K_a in kdowns) - (K_z in kdowns or K_SEMICOLON in kdowns)),
	])
	if K_j in kdowns and len(cpools) == 2:
		jp0, jp1 = cpools
		joiners.append({ "jp0": jp0, "jp1": jp1, "w": 2, "waypoints": [] })
		cjoin = len(joiners) - 1
	if K_p in kdowns and len(cpools) == 2:
		jp0, jp1 = cpools
		if pools[jp0]["pos"][2] > pools[jp1]["pos"][2]:
			jp0, jp1 = jp1, jp0
		pipes.append({ "jp0": jp0, "jp1": jp1 })
	for r, K in [(0, K_e), (5, K_w)]:
		if K in kdowns and cjoin is not None:
			joiner = joiners[cjoin]
			jp0 = joiner["jp0"]
			jp1 = joiner["jp1"]
			waypoints = joiner["waypoints"]
			ps = list(map(Vector3, [pools[jp0]["pos"]] + [p for p, r in waypoints] + [pools[jp1]["pos"]]))
			if jp0 in cpools:
				p = (ps[0] + ps[1]) / 2
				p.z = ps[0].z
				waypoints.insert(0, (tuple(p), r))
			else:
				p = (ps[-2] + ps[-1]) / 2
				p.z = ps[-1].z
				waypoints.append((tuple(p), r))
	if K_s in kdowns and cjoin:
		waypoints = joiners[cjoin]["waypoints"]
		for k, ((x, y, z), r) in enumerate(waypoints):
			x += random.uniform(-10, 10)
			y += random.uniform(-10, 10)
			z += random.uniform(-10, 10)
			waypoints[k] = (x, y, z), r
	if K_n in kdowns:
		p = list(map(int, p0))
		pools.append({ "pos": p, "r": 10, "pressure": 3, "drainable": False })
	if K_1 in kdowns:
		for jpool in cpools:
			pools[jpool]["r"] = pvalue(rpools, pools[jpool]["r"])
		for j, k in cway:
			p, r = joiners[j]["waypoints"][k]
			joiners[j]["waypoints"][k] = p, pvalue(rways, r, wrap=False)
		if cjoin is not None:
			joiners[cjoin]["w"] = pvalue(rpools, joiners[cjoin]["w"], wrap=False)
	if K_2 in kdowns:
		if cjoin is not None:
			joiners[cjoin]["w"] = nvalue(rpools, joiners[cjoin]["w"], wrap=False)
		else:
			for jpool in cpools:
				pools[jpool]["r"] = nvalue(rpools, pools[jpool]["r"])
		for j, k in cway:
			p, r = joiners[j]["waypoints"][k]
			joiners[j]["waypoints"][k] = p, nvalue(rways, r, wrap=False)
	if K_3 in kdowns:
		for j, k in cway:
			joiner = joiners[j]
			p, r = joiner["waypoints"][k]
			p0s = [pools[jp0]["pos"]] + [p0 for p0, r0 in joiner["waypoints"]] + [pools[jp1]["pos"]]
			z0 = p0s[k][2]
			z1 = p0s[k+2][2]
			p = p[0], p[1], (z1 if p[2] == z0 else z0)
			joiner["waypoints"][k] = p, r
	if K_4 in kdowns:
		for jpool in cpools:
			pools[jpool]["pressure"] = pvalue(pressures, pools[jpool]["pressure"], wrap=False)
	if K_5 in kdowns:
		for jpool in cpools:
			pools[jpool]["pressure"] = nvalue(pressures, pools[jpool]["pressure"], wrap=False)
	if K_6 in kdowns:
		for jpool in cpools:
			pools[jpool]["drainable"] = not pools[jpool]["drainable"]
	if K_RETURN in kdowns:
		for j, joiner in enumerate(joiners):
			waypoints = joiner["waypoints"]
			jp0 = joiner["jp0"]
			jp1 = joiner["jp1"]
			pool0 = pools[jp0]
			pool1 = pools[jp1]
			n = len(waypoints)
			# Fix waypoint z-coordinate.
			# z-coordinate can only change between consecutive waypoints if they both have radius 0.
			zrs = [(pool0["pos"][2], None)] + [(z, r) for (x, y, z), r in waypoints] + [(pool1["pos"][2], None)]
			zsections = []
			last0 = False
			for k, (z, r) in enumerate(zrs):
				if k == 0:
					zsections.append((z, [k]))
					last0 = False
				else:
					z0, ks = zsections[-1]
					if r is None or r > 0:
						ks.append(k)
						last0 = False
					else:
						if last0:
							zsections.append((z, [k]))
						else:
							ks.append(k)
						last0 = True
			print(zsections)
			if len(zsections) == 1 and zsections[-1][0] != zrs[-1][0]:
				print("Unable to fix joiner %d: %s" % (k, joiner))
				continue
			zsections[-1] = zrs[-1][0], zsections[-1][1]
			for z, ks in zsections:
				for k in ks:
					if k in (0, n + 1):
						continue
					(x, y, _), r = waypoints[k-1]
					waypoints[k-1] = (x, y, z), r
			# Fix waypoint x-y coordinate.
			# Direction in the x-y plane can only change at a waypoint if it has positive radius.
			xyrs = [(pool0["pos"][0], pool0["pos"][1], None)] + [(x, y, r) for (x, y, z), r in waypoints] + [(pool1["pos"][0], pool1["pos"][1], None)]
			xysections = []
			for k, (x, y, r) in enumerate(xyrs):
				if k == 0:
					xysections.append([])
				xysections[-1].append((x, y, k))
				if r is not None and r > 0:
					xysections.append([])
					xysections[-1].append((x, y, k))
			for xysection in xysections:
				x0, y0, _ = xysection[0]
				x1, y1, _ = xysection[-1]
				for x, y, k in xysection[1:-1]:
					x, y = xysnap((x0, y0), (x1, y1), (x, y))
					(_, _, z), r = waypoints[k-1]
					waypoints[k-1] = (x, y, z), r
	for jpool in cpools:
		pools[jpool]["pos"] = tuple(Vector3(pools[jpool]["pos"]) + vscoot)
	for j, k in cway:
		p, r = joiners[j]["waypoints"][k]
		joiners[j]["waypoints"][k] = tuple(Vector3(p) + vscoot), r
	if mright:
		phi += 0.01 * dmx
		theta -= 0.01 * dmy
		theta = min(max(theta, 0), math.pi / 2)
	if mcenter:
		pd = 2 * Vector3(dmx, -dmy, 0) / zoom
		p0 -= pd.rotate_x(math.degrees(theta)).rotate_z(-math.degrees(phi))
	if scroll:
		zoom *= math.exp(0.1 * scroll)
	if K_o in kdowns:
		theta = 1
		phi = 0

	screen.fill((0, 0, 0))
	
	for jpool, pool in enumerate(pools):
		pos = Vector3(pool["pos"])
		r = pool["r"]
		pressure = pool["pressure"]
		drainable = pool["drainable"]
		drawpoint(pos, 0.3, [255, 255, 255])
		color = (255, 200, 200) if jpool in cpools else (255, 0, 0)
		for dz in (-r / 4, r / 4):
			drawellipse(pos + Vector3(0, 0, dz), r, color)
		color = (200, 200, 200) if jpool in cpools else (30, 30, 30)
		text = "\n".join([
			"%d" % jpool,
			"%d" % r,
			"",
			"%.0f,%.0f,%.0f" % tuple(pos),
			"%d %s" % (pressure, drainable)
		])
		ptext.draw(text, center = screenpos(pos), fontsize = 18, color = color, owidth = 2)
	for jjoin, joiner in enumerate(joiners):
		jp0 = joiner["jp0"]
		jp1 = joiner["jp1"]
		waypoints = [p for p, r in joiner["waypoints"]]
		p0s = list(map(Vector3, [pools[jp0]["pos"]] + waypoints + [pools[jp1]["pos"]]))
		color = (100, 100, 255) if jjoin == cjoin else (0, 0, 100)
		jcurves = [True] + [r > 0 for p, r in joiner["waypoints"]] + [True]
		ps = [p0s[0]]
		for j, (pB, r) in enumerate(joiner["waypoints"]):
			j0, j1, j2 = j, j + 1, j + 2
			while not jcurves[j0]: j0 -= 1
			while not jcurves[j2]: j2 += 1
			pA, pB, pC = p0s[j0], p0s[j1], p0s[j2]
			if r == 0:
				ps.append(pB)
			else:
				def toxy(v):
					return Vector3(v.x, v.y, 0)
				f0 = toxy(pB - pA)
				f1 = toxy(pC - pB)
				if f0.length() == 0 or f1.length == 0:
					ps.append(pB)
					continue
				f0 = f0.normalize()
				f1 = f1.normalize()
				if abs(f0.dot(f1)) > 0.999:
					ps.append(pB)
					continue
				f = (f1 - f0).normalize()
				z = f1.cross(f0).normalize()
				beta = 1/2 * math.acos(f0.dot(f1))
				center = pB + f * r / math.cos(beta)
				for jbeta in range(-5, 6):
					zeta = jbeta / 5 * beta
					ps.append(center - r * f.rotate(-math.degrees(zeta), z))
		ps += [p0s[-1]]
		for j in range(len(ps) - 1):
			drawwideline(ps[j], ps[j+1], joiner["w"], color)
		for k, (p, r) in enumerate(joiner["waypoints"]):
			color = (255, 255, 255) if (jjoin, k) in cway else (0, 0, 200)
			drawpoint(p, 0.1, color)
			text = "\n".join(["%d,%d" % (jjoin, k), "", "%.0f,%.0f,%.0f %.0f" % (p[0], p[1], p[2], r)])
			ptext.draw(text, center = screenpos(p), fontsize = 18, color = color, owidth = 2)
	for jpipe, pipe in enumerate(pipes):
		jp0 = Vector3(pools[pipe["jp0"]]["pos"])
		jp1 = Vector3(pools[pipe["jp1"]]["pos"])
		drawline(jp0, jp1, (100, 100, 0))
	
	text = [
		"Left click: select pools and waypoints",
		"Shift + left click: select multiple pools and waypoints",
		"Space: cycle pool selection",
		"Scroll wheel: zoom",
		"Right drag: rotate",
		"Middle drag: move viewport",
		"Arrow keys + A/Z: move selected pools/waypoints",
		"N: new pool",
#		"Ctrl + Arrow keys/A/Z: move viewport",
		"O: reset orientation",
		"Enter: fix waypoint positions",
	]
	if cjoin is None:
		text.append("To select a joiner: select a single pool and press Tab")
	else:
		text.append("1/2: adjust selected joiner width")
		text.append("W: add waypoint to currently selected joiner")
		text.append("E: add zero-radius waypoint to currently selected joiner")
		text.append("S: scatter waypoints of selected joiner")
	if cpools:
		text.append("1/2: adjust selected pool size")
		text.append("4/5: adjust selected pool pressure")
		text.append("6: toggle selected pool drainability")
	if cway:
		text.append("1/2: adjust selected waypoint radii")
		text.append("3: align selected waypoint z-value")
	if len(cpools) == 2:
		text.append("J: add joiner between selected pools")
		text.append("P: add pipe from lower pool to upper pool")
	else:
		text.append("Select 2 pools at once to create a joining tunnel")
		text.append("Select 2 pools on different levels to create a pipe")

	ptext.draw("\n".join(text), bottomleft = (2, screen.get_height() - 2), fontsize = 21, owidth = 2)

	pygame.display.flip()
	save()

dump()

