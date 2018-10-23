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
"""


import sys, pygame, math, json, os, sys
from pygame.locals import *
from pygame.math import Vector2, Vector3
from . import ptext

savefile = "/tmp/flow.json"


zoom = 1
p0 = Vector3(0, 0, 0)

# ISO convention https://en.wikipedia.org/wiki/Spherical_coordinate_system
theta = 1
phi = 0

w, h = 1024, 720
screen = pygame.display.set_mode((w, h))

# previous value  within sorted list vs less than v
def pvalue(vs, v):
	xs = [x for x in vs if x < v]
	return xs[-1] if xs else vs[-1]
# next value within sorted list vs greater than v
def nvalue(vs, v):
	xs = [x for x in vs if x > v]
	return xs[0] if xs else vs[0]

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
	w = max(2, int(round(r * zoom)))
	h = max(2, int(round(r * zoom * math.cos(theta))))
	rect = pygame.Rect((0, 0, w, h))
	rect.center = screenpos(pos)
	pygame.draw.ellipse(screen, color, rect, 1)
def drawline(p0, p1, color):
	pygame.draw.line(screen, color, screenpos(p0), screenpos(p1))

rpools = 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 17, 20, 22, 25, 27, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100
pools = [
	{ "pos": (5, 5, 0), "r": 10, },
	{ "pos": (5, 5, 20), "r": 8, },
	{ "pos": (40, 40, 0), "r": 8, },
]
joiners = [
	{ "jp0": 0, "jp1": 2, "waypoints": [(5, 40, 0),], },
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
			for k, waypoint in enumerate(joiner["waypoints"])
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
		joiners.append({ "jp0": jp0, "jp1": jp1, "waypoints": [] })
		cjoin = len(joiners) - 1
	if K_p in kdowns and len(cpools) == 2:
		jp0, jp1 = cpools
		pipes.append({ "jp0": jp0, "jp1": jp1 })
	if K_w in kdowns and cjoin is not None:
		joiner = joiners[cjoin]
		jp0 = joiner["jp0"]
		jp1 = joiner["jp1"]
		waypoints = joiner["waypoints"]
		ps = list(map(Vector3, [pools[jp0]["pos"]] + waypoints + [pools[jp1]["pos"]]))
		if jp0 in cpools:
			p = tuple((ps[0] + ps[1]) / 2)
			waypoints.insert(0, p)
		else:
			p = tuple((ps[-2] + ps[-1]) / 2)
			waypoints.append(p)
	if K_n in kdowns:
		p = list(map(int, p0))
		pools.append({ "pos": p, "r": 10, })
	if K_1 in kdowns:
		for jpool in cpools:
			pools[jpool]["r"] = pvalue(rpools, pools[jpool]["r"])
	if K_2 in kdowns:
		for jpool in cpools:
			pools[jpool]["r"] = nvalue(rpools, pools[jpool]["r"])


	for jpool in cpools:
		pools[jpool]["pos"] = tuple(Vector3(pools[jpool]["pos"]) + vscoot)
	for j, k in cway:
		joiners[j]["waypoints"][k] = tuple(Vector3(joiners[j]["waypoints"][k] + vscoot))
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
		drawpoint(pos, 0.3, [255, 255, 255])
		color = (255, 200, 200) if jpool in cpools else (255, 0, 0)
		for dz in (-r / 4, r / 4):
			drawellipse(pos + Vector3(0, 0, dz), r, color)
		color = (200, 200, 200) if jpool in cpools else (30, 30, 30)
		text = "\n".join(["%d" % jpool, "", "%.0f,%.0f,%.0f" % tuple(pos)])
		ptext.draw(text, center = screenpos(pos), fontsize = 18, color = color, owidth = 2)
	for jjoin, joiner in enumerate(joiners):
		jp0 = joiner["jp0"]
		jp1 = joiner["jp1"]
		waypoints = joiner["waypoints"]
		ps = list(map(Vector3, [pools[jp0]["pos"]] + waypoints + [pools[jp1]["pos"]]))
		color = (100, 100, 255) if jjoin == cjoin else (0, 0, 100)
		for j in range(len(ps) - 1):
			drawline(ps[j], ps[j+1], color)
		for k, p in enumerate(waypoints):
			color = (255, 255, 255) if (jjoin, k) in cway else (0, 0, 200)
			drawpoint(p, 0.1, color)
	for jpipe, pipe in enumerate(pipes):
		jp0 = Vector3(pools[pipe["jp0"]]["pos"])
		jp1 = Vector3(pools[pipe["jp1"]]["pos"])
		drawline(jp0, jp1, (100, 100, 0))
	
	text = [
		"Left click: select pools and waypoints",
		"Shift + left click: select multiple pools and waypoints",
		"Scroll wheel: zoom",
		"Right drag: rotate",
		"Middle drag: move viewport",
		"Arrow keys + A/Z: move selected pools/waypoints",
		"N: new pool",
#		"Ctrl + Arrow keys/A/Z: move viewport",
		"O: reset orientation",
	]
	if cjoin is None:
		text.append("To select a joiner: select a single pool and press Tab")
	else:
		text.append("W: add waypoint to currently selected joiner")
	if cpools:
		text.append("1/2: adjust selected pool size")
	if len(cpools) == 2:
		text.append("J: add joiner between selected pools")
		text.append("P: add pipe from lower pool to upper pool")
	else:
		text.append("Select 2 pools at once to create a joining tunnel")
		text.append("Select 2 pools on different levels to create a pipe")

	ptext.draw("\n".join(text), bottomleft = (2, screen.get_height() - 2), fontsize = 21, owidth = 2)

	pygame.display.flip()
	save()


