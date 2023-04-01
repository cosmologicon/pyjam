import pygame, sys
from . import maff, view, pview, grid, control, ptext, thing, levels
from .pview import T

levelname = "0"
if len(sys.argv) > 1:
	levelname = sys.argv[1]
view.VscaleG = 20
view.init()

floor = set([(0, 0)])
goals = set()
obstacles = {}
lights = {}
you = None

if levelname in levels.levels:
	obj = levels.levels[levelname]
	floor = obj["floor"]
	goals = obj["goals"]
	obstacles = obj["obstacles"]
	lights = obj["lights"]
	you = obj["you"]


ldirs = [[(1, 0)], [(0, 1)], [(-1, 1)], [(-1, 0)], [(0, -1)], [(1, -1)]]
for j in range(6):
	ldirs.append(ldirs[j] + ldirs[(j + 1) % 6])
for j in range(6):
	ldirs.append(ldirs[j] + ldirs[(j + 2) % 6])
ldirs.append([d for ldir in ldirs[:6] for d in ldir])

clock = pygame.time.Clock()
playing = True
cursorH = None
while playing:
	dt = clock.tick(120) * 0.001
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_1 and cursorH:
				you = cursorH
			if event.key == pygame.K_2 and cursorH:
				if cursorH in goals:
					goals.remove(cursorH)
				else:
					goals.add(cursorH)
			if event.key == pygame.K_p and cursorH:
				obstacles[cursorH] = "P"
			if event.key == pygame.K_b and cursorH:
				obstacles[cursorH] = "B"
			if event.key == pygame.K_u and cursorH:
				obstacles[cursorH] = "U"
			if event.key == pygame.K_d and cursorH:
				obstacles[cursorH] = "D"
			if event.key == pygame.K_TAB and cursorH:
				if cursorH not in lights:
					lights[cursorH] = ldirs[0]
				else:
					j = ldirs.index(lights[cursorH]) + 1
					if j >= len(ldirs):
						del lights[cursorH]
					else:
						lights[cursorH] = ldirs[j]
				
	control.think(dt)
	cursorH = grid.HnearestG(control.mposG)
	kpressed = pygame.key.get_pressed()
	if kpressed[pygame.K_SPACE]:
		floor.add(cursorH)
	if kpressed[pygame.K_BACKSPACE]:
		if cursorH in floor:
			floor.remove(cursorH)
		if cursorH in goals:
			goals.remove(cursorH)
		if cursorH == you:
			you = None
		if cursorH in obstacles:
			del obstacles[cursorH]
		if cursorH in lights:
			del lights[cursorH]
	pview.fill((0, 0, 0))
	colors = (160, 160, 160), (170, 170, 130), (150, 150, 190)
	for x, y in floor:
		pVs = [view.VconvertG(pG) for pG in grid.GoutlineH((x, y))]
		color = colors[(x - y) % 3]
		pygame.draw.polygon(pview.screen, color, pVs)
	pVs = [view.VconvertG(pG) for pG in grid.GoutlineH(cursorH)]
	pygame.draw.polygon(pview.screen, (255, 255, 0), pVs, 1)
	for goal in goals:
		thing.drawcircleat(goal, 0.2, (0, 255, 0))
	for pos, name in obstacles.items():
		pV = view.VconvertG(grid.GconvertH(pos))
		ptext.draw(name, center = pV, fontsize = T(20), owidth = 0.5)
	for (x, y), dirHs in lights.items():
		pV0 = view.VconvertG(grid.GconvertH((x, y)))
		for dx, dy in dirHs:
			pV1 = view.VconvertG(grid.GconvertH((x + dx, y + dy)))
			pygame.draw.line(pview.screen, (255, 50, 50), pV0, pV1, 2)
		thing.drawcircleat((x, y), 0.2, (255, 0, 0))
	if you:
		thing.drawcircleat(you, 0.5, (255, 128, 0))

	text = "\n".join([
		f"Level: {levelname}",
		"Hold space: add floor",
		"Hold backspace: clear",
		"1: set starting position",
		"2: place goal",
		"Tab: place/rotate light",
		"P: place pawn",
		"B: place bishop",
		"U: place urook",
		"D: place drook",
		f"{cursorH[0], cursorH[1]}"
	])
	ptext.draw(text, T(0, 0), fontsize = T(24), owidth=0.5)
	pygame.display.flip()

obj = {
	"floor": floor,
	"goals": goals,
	"obstacles": obstacles,
	"lights": lights,
	"you": you,
}
print(f"""levels["{levelname}"] = {obj}""")


