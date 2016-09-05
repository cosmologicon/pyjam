import pygame, math
from . import ptext, progress
from .util import F

lines = {
	"intro0": [
		["A", "Hello and welcome to my lab."],
		["A", "Today we will make cells."],
	],
}


queue = []
playing = None
tquiet = 0

def quiet():
	return not playing and not queue

def play(dname):
	if dname in progress.heard:
		return
	progress.heard.add(dname)
	queue.extend(lines[dname])

def think(dt):
	global tquiet, playing, tplaying
	if quiet():
		tquiet += dt
	else:
		tquiet = 0
	if queue and not playing:
		playing = queue.pop(0)
		tplaying = 0
	if playing:
		tplaying += dt
		if tplaying > 0.05 * len(playing[1]):
			playing = None

def draw():
	if playing:
		who, line = playing
		alpha = math.clamp(4 * tplaying, 0, 1)
		ptext.draw(line, midbottom = F(854 / 2, 470),
			color = (255, 100, 255), shadow = (1, 1),
			fontsize = F(36))


