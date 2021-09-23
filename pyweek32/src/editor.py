import pygame, math, pickle, os.path
from . import ptext, geometry, pview, maff
from .pview import T



points = []
walls = []
regions = []
locks = []
objs = {}
checkpoints = {}

savename = "gamemap.pkl"
def save():
	obj = points, walls, regions, locks, objs, checkpoints
	pickle.dump(obj, open(savename, "wb"))
def load():
	global points, walls, regions, locks, objs, checkpoints
	if os.path.exists(savename):
		obj = pickle.load(open(savename, "rb"))
		points, walls, regions, locks, objs, checkpoints = obj
load()


pview.set_mode((1280, 720))

vx0, vy0, scale = 0, 0, 3
objtypes = ["-", "+", "key", "X", "bigL", "bigR", "2", "3", "L", "R", "2L", "2R", "4", "4L", "4R"]

def gamepos(screenpos):
	px, py = screenpos
	return vx0 + (px - pview.centerx) / scale, vy0 - (py - pview.centery) / scale
def screenpos(gamepos):
	x, y = gamepos
	return T(pview.centerx + scale * (x - vx0), pview.centery - scale * (y - vy0))
def screenscale(d):
	return T(d * scale)

fig8 = [(80 * C / (1 + S ** 2), 80 * S * C / (1 + S ** 2)) for C, S in math.CSround(120)]
rcolors = [tuple([math.imix(20, 50, math.fuzz(j, k)) for j in range(3)]) for k in range(40)]

pointed = None
wallstart = None
tregion = []

playing = True
while playing:
	kpressed = pygame.key.get_pressed()
	kdowns = set()
	mdowns = set()
	mups = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			kdowns.add(event.key)
		if event.type == pygame.MOUSEBUTTONDOWN:
			mdowns.add(event.button)
		if event.type == pygame.MOUSEBUTTONUP:
			mups.add(event.button)

	if pygame.K_ESCAPE in kdowns:
		playing = False

	mpos = gamepos(pygame.mouse.get_pos())
	pointed = min(points, key = lambda p: math.distance(p, mpos)) if points else None
	if pointed is not None and math.distance(pointed, mpos) > 16:
		pointed = None
	
	if pygame.K_BACKSPACE in kdowns:
		if pointed is not None:
			points.remove(pointed)
			walls = [wall for wall in walls if pointed not in wall]
			regions = [region for region in regions if pointed not in regions]
			if pointed in checkpoints:
				del checkpoints[pointed]
			if pointed in locks:
				locks.remove(pointed)
			if pointed in objs:
				del objs[pointed]
	if pygame.K_3 in kdowns:
		if pointed is not None:
			checkpoints[pointed] = (checkpoints[pointed] + 1) % 24 if pointed in checkpoints else 0
	if pygame.K_4 in kdowns:
		if pointed in locks:
			locks.remove(pointed)
		else:
			locks.append(pointed)
	if pygame.K_5 in kdowns:
		if regions:
			regions.pop()

	if 1 in mdowns:
		if kpressed[pygame.K_SPACE]:
			if pointed is None:
				tregion = []
			elif tregion and tregion[0] == pointed:
				regions.append(tregion)
				tregion = []
			else:
				tregion.append(pointed)
		else:
			points.append(mpos)
			if kpressed[pygame.K_1]:
				x, y = mpos
				points.append((-x, -y))
			if kpressed[pygame.K_2]:
				x, y = mpos
				points.append((-x, y))
	if 2 in mdowns:
		vx0, vy0 = mpos
	if 3 in mdowns and wallstart is None:
		wallstart = pointed
	if 3 in mups and wallstart is not None:
		if wallstart == pointed:
			if pointed in objs and objs[pointed] in objtypes:
				j = objtypes.index(objs[pointed]) + 1
				if j < len(objtypes):
					objs[pointed] = objtypes[j]
				else:
					del objs[pointed]
			else:
				objs[pointed] = objtypes[0]
		elif pointed is not None:
			walls.append((wallstart, pointed))
		wallstart = None
	dwheel = (4 in mdowns) - (5 in mdowns)
	if dwheel:
		scale *= math.exp(0.1 * dwheel)
		


	if kdowns or mdowns:
		save()

	pview.fill((0, 0, 0))
	for p in fig8:
		pygame.draw.circle(pview.screen, (10, 10, 10), screenpos(p), screenscale(14))
	for region, rcolor in zip(regions, rcolors):
		pygame.draw.polygon(pview.screen, rcolor, [screenpos(p) for p in region])
	px0, py0 = screenpos((0, 0))
	pygame.draw.line(pview.screen, (40, 40, 40), (0, py0), (pview.w, py0))
	pygame.draw.line(pview.screen, (40, 40, 40), (px0, 0), (px0, pview.h))

	for p0, p1 in walls + ([] if wallstart is None else [(wallstart, mpos)]):
		color = (120, 40, 40)
		pygame.draw.line(pview.screen, color, screenpos(p0), screenpos(p1))
	for point in points:
		if point == pointed:
			color = (255, 255, 255)
		elif point in checkpoints:
			color = (100, 200, 100)
		elif point in locks:
			color = (255, 255, 0)
		else:
			color = (100, 100, 100)
		pygame.draw.circle(pview.screen, color, screenpos(point), screenscale(1))
		if point in checkpoints:
			pos = math.CS(math.tau / 4 - checkpoints[point] * math.tau / 24, 3, center = point)
			pygame.draw.line(pview.screen, color, screenpos(point), screenpos(pos))

	for point in objs:
		x, y = point
		ptext.draw(objs[point], center = screenpos((x, y + 2)), fontsize = T(16), owidth = 1)
			

	if tregion:
		for pos in tregion:
			pygame.draw.circle(pview.screen, (200, 200, 255), screenpos(pos), screenscale(1.6), 1)
		


	text = "\n".join([
		("mpos None") if mpos is None else ("mpos (%.1f, %.1f)" % mpos),
		"left click: place point",
		"right click: assign obj",
		"right drag: place wall",
		"hold space + left click: trace region",
		"backspace: remove point",
		"hold 1: mirror point",
		"hold 2: horiz mirror point",
		"3: assign checkpoint",
		"4: assign lock",
		"5: pop region",
		"middle click: recenter",
		"mouse wheel: zoom",
	])
	ptext.draw(text, bottomleft = (4, pview.h - 4), fontsize = 22, owidth = 1)
	
	pygame.display.flip()

save()

