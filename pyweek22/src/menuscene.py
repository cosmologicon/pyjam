import random, math, pygame
from . import ptext, view, scene, playscene, cutscene, blob
from .util import F


def init():
	global levels, pointed
	levels = {
		0: [100, 100],
		1: [300, 160],
		2: [100, 250],
	}
	pointed = None


def think(dt, mpos, mdown, mup, *args):
	global pointed
	mx, my = mpos
	for jlevel, pos in levels.items():
		x, y = F(pos)
		if (x - mx) ** 2 + (y - my) ** 2 < F(30) ** 2:
			pointed = jlevel
			break
	else:
		pointed = None
	if pointed is not None and mdown:
		level = pointed
		scene.pop()
		scene.push(playscene)
		scene.push(cutscene.Start())

def draw():
	view.clear(color = (20, 80, 20))
	for jlevel, pos in levels.items():
		pygame.draw.circle(view.screen, (255, 255, 255), F(pos), F(30), F(1))
	if pointed is not None:
		text = "Level %s" % pointed
		ptext.draw(text, fontsize = F(80), midbottom = F(854 / 2, 470),
			color = "white", gcolor = (50, 50, 50), shadow = (1, 1))

def abort():
	pass

