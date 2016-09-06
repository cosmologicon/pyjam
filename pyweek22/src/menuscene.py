import random, math, pygame
from . import ptext, view, scene, playscene, cutscene, blob, progress, level, settings
from .util import F


def init():
	global levels, pointed, blobspecs
	levels = {
		0: [100, 100],
		1: [240, 130],
		2: [100, 250],
		"endless": [800, 300],
		"qwin": [800, 400],
	}
	pointed = None
	blobspecs = dict((lname, [(
		random.uniform(0, math.tau),
		random.uniform(0.6, 1) * random.choice([-1, 1]),
		random.uniform(0.2, 1.2),
	) for j in range(30)]) for lname in levels)


def think(dt, mpos, mdown, mup, *args):
	global pointed
	mx, my = mpos
	for jlevel, pos in levels.items():
		if jlevel not in progress.unlocked:
			continue
		x, y = F(pos)
		if (x - mx) ** 2 + (y - my) ** 2 < F(40) ** 2:
			pointed = jlevel
			break
	else:
		pointed = None
	if pointed is not None and mdown:
		progress.setchosen(pointed)
		scene.pop()
		scene.push(playscene)
		scene.push(cutscene.Start())

def draw():
	view.clear(color = (20, 80, 20))
	for level0, nlevels in level.unlocks.items():
		for level1 in nlevels:
			if level0 in progress.unlocked and level1 in progress.unlocked:
				p0 = F(levels[level0])
				p1 = F(levels[level1])
				t1 = F(24)
				t0 = F(12)
				pygame.draw.line(view.screen, (0, 0, 0), p0, p1, t1)
				pygame.draw.line(view.screen, (100, 255, 100), p0, p1, t0)
	ptext.draw(settings.gamename, fontsize = F(50), topright = F(834, 20),
		color = "yellow", owidth = 1)
	for j, (jlevel, pos) in enumerate(sorted(levels.items())):
		if jlevel not in progress.unlocked:
			continue
		a = 30
		hillspec = []
		for theta0, dtheta, fr in blobspecs[jlevel]:
			theta = theta0 + 0.001 * pygame.time.get_ticks() * dtheta
			x, y = pos
			x = F(x + fr * a * math.sin(theta))
			y = F(y + fr * a * math.cos(theta))
			hillspec.append((x, y, F(a), 0.5))
		blob.drawcell(view.screen, hillspec)
		text = "%s" % jlevel
		ptext.draw(text, fontsize = F(30), center = F(pos),
			color = "white", shadow = (1, 1))
	if pointed is not None:
		text = "Level %s" % pointed
		ptext.draw(text, fontsize = F(80), midbottom = F(854 / 2, 470),
			color = "white", gcolor = (50, 50, 50), shadow = (1, 1))

def abort():
	pass

