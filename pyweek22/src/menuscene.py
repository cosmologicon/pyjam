import random, math, pygame
from . import ptext, view, scene, playscene, cutscene, blob, progress, level, settings, sound
from .util import F


message = None
tmessage = 0

def init():
	global levels, pointed, blobspecs, message, tmessage
	pointed = None
	blobspecs = dict((lname, [(
		random.uniform(0, math.tau),
		random.uniform(0.6, 1) * random.choice([-1, 1]),
		random.uniform(0.2, 1.2),
	) for j in range(30)]) for lname in level.layout)
	sound.playmusic("menu")

	blobspecs["title1"] = [(
		random.uniform(0, math.tau),
		random.uniform(0.6, 1) * random.choice([-1, 1]),
		random.uniform(0.2, 1.2),
	) for j in range(30)]
	blobspecs["title2"] = [(
		random.uniform(0, math.tau),
		random.uniform(0.6, 1) * random.choice([-1, 1]),
		random.uniform(0.2, 1.2),
	) for j in range(30)]

def setmessage(m):
	global message, tmessage
	message = m
	tmessage = 8

def think(dt, mpos, mdown, mup, *args):
	global pointed, tmessage
	mx, my = mpos
	for jlevel, (r, x, y) in level.layout.items():
		if jlevel not in progress.unlocked:
			continue
		x, y = F((x, y))
		if (x - mx) ** 2 + (y - my) ** 2 < F(r) ** 2:
			pointed = jlevel
			break
	else:
		pointed = None
	if pointed is not None and mdown:
		progress.setchosen(pointed)
		scene.pop()
		scene.push(playscene)
		scene.push(cutscene.Start())
	if tmessage:
		tmessage = max(0, tmessage - dt)

def draw():
	view.clear(color = (20, 80, 20))
	for level0, nlevels in level.unlocks.items():
		for level1 in nlevels:
			if level0 in progress.unlocked and level1 in progress.unlocked:
				p0 = F(level.layout[level0][1:3])
				p1 = F(level.layout[level1][1:3])
				t1 = F(24)
				t0 = F(12)
				pygame.draw.line(view.screen, (0, 0, 0), p0, p1, t1)
				pygame.draw.line(view.screen, (100, 255, 100), p0, p1, t0)
	ptext.draw("Dr. Zome's", fontsize = F(45), fontname = "SansitaOne",
		topright = F(834, 10),
		color = "yellow", owidth = 1)
	ptext.draw("Lab   rat   ry", fontsize = F(60), fontname = "SansitaOne",
		topright = F(834, 50),
		color = "yellow", owidth = 1)
	for (x0, y0, name) in [(615, 95, "title1"), (745, 95, "title2")]:
		hillspec = []
		for theta0, dtheta, fr in blobspecs[name]:
			theta = theta0 + 0.001 * pygame.time.get_ticks() * dtheta
			x = F(x0 + fr * 15 * math.sin(theta))
			y = F(y0 + fr * 15 * math.cos(theta))
			hillspec.append((x, y, F(15), 0.5))
		blob.drawcell(view.screen, hillspec, color = (100, 100, 0))


	for j, (jlevel, (a, px, py)) in enumerate(sorted(level.layout.items(), key = str)):
		if jlevel not in progress.unlocked:
			continue
		hillspec = []
		for theta0, dtheta, fr in blobspecs[jlevel]:
			theta = theta0 + 0.001 * pygame.time.get_ticks() * dtheta
			x, y = px, py
			x = F(x + fr * a * math.sin(theta))
			y = F(y + fr * a * math.cos(theta))
			hillspec.append((x, y, F(a), 0.5))
		blob.drawcell(view.screen, hillspec)
		text = "%s" % jlevel
		ptext.draw(text, fontsize = F(30), center = F(px, py),
			color = "white", shadow = (1, 1))
	if pointed is not None:
		text = "Level %s" % pointed
		ptext.draw(text, fontsize = F(80), midbottom = F(854 / 2, 470),
			color = "white", gcolor = (50, 50, 50), shadow = (1, 1))
	if tmessage:
		alpha = min(tmessage * 2, 1)
		ptext.draw(message, fontsize = F(60), center = F(854 / 2, 200), width = F(500),
			color = "#FF7F7F", shadow = (1, 1), alpha = alpha)

def abort():
	pass

