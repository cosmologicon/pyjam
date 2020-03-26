from . import maff
import sys, pygame, json
from . import control, settings, ptext, pview, thing, view


control.init()
w = int(sys.argv[1])
h = int(sys.argv[2])
pview.set_mode((1280, 720))
x, y = 0, 0
view.cx = w / 2
view.cy = h / 2
view.zoom = min(100, 720 / h)

leps = []

def pickany(objs):
	objs = list(objs)
	return objs[0] if objs else None

def lepat(pos):
	return pickany(lep for lep in leps if (lep.x, lep.y) == pos)

def swapat(pos):
	lep0 = lepat(pos)
	if lep0:
		leps.remove(lep0)
	if lep0 is None:
		leps.append(thing.FlowLep(pos, []))
	elif isinstance(lep0, thing.FlowLep):
		leps.append(thing.GoalLep(pos))
	else:
		pass

def swapdirat(pos, d):
	lep = lepat(pos)
	print(pos, d, lep)
	if lep:
		if d in lep.ds:
			lep.ds.remove(d)
		else:
			lep.ds.append(d)
		print(lep.ds)

def output():
	state = {
		"w": w,
		"h": h,
		"goal": [{"x": lep.x, "y": lep.y} for lep in leps if isinstance(lep, thing.GoalLep)],
		"flow": [{"x": lep.x, "y": lep.y, "ds": lep.ds}
			for lep in leps if isinstance(lep, thing.FlowLep)],
	}
	print(json.dumps(state))
	print()
		

clock = pygame.time.Clock()
playing = True
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	
	kpressed = pygame.key.get_pressed()
	shift = kpressed[pygame.K_SPACE]
	for keys in control.get():
		if "quit" in keys:
			playing = False
		if "forfeit" in keys:
			output()
		if "screenshot" in keys:
			pview.screenshot()
		if "combo" in keys:
			dx = int("right" in keys) - int("left" in keys)
			dy = int("up" in keys) - int("down" in keys)
			if shift:
				if dx or dy:
					swapdirat((x, y), (dx, dy))
			else:
				x += dx
				y += dy
		if "swap" in keys:
			swapat((x, y))

	pview.fill((40, 40, 40) if shift else (30, 30, 30))

	rect = pygame.Rect(pview.I(0, 0, 1.3 * view.zoom, 1.3 * view.zoom))
	rect.center = view.worldtoscreen((x + 0.5, y + 0.5))
	pygame.draw.rect(pview.screen, (60, 60, 60), rect)

	gridlines = [((x, 0), (x, h)) for x in range(0, w + 1)]
	gridlines += [((0, y), (w, y)) for y in range(0, h + 1)]
	for p0, p1 in gridlines:
		pygame.draw.line(pview.screen, (50, 50, 140),
			view.worldtoscreen(p0), view.worldtoscreen(p1), 1)
	for lep in leps:
		lep.draw()

	text = "\n".join([
		"%.1ffps" % clock.get_fps(),
		"pos %d %d" % (x, y),
	])
	ptext.draw(text, bottomleft = pview.bottomleft, fontsize = 24, owidth = 1)
	pygame.display.flip()

output()

