import pygame, math
from . import ptext, progress, img
from .util import F

lines = {
	"intro0": [
		["Zbounce", "Hello and welcome to my lab."],
		["Ssink", "Today we will make cells."],
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
		t = pygame.time.get_ticks() * 0.001
		h = 390 - 20 * abs(math.sin(12 * t)) if "bounce" in who else 400
		angle = 10 * math.sin(6 * t) if "rock" in who else 0
		fstretch = math.exp(0.1 - 0.02 * tplaying) if "sink" in who else 1
		if "Z" in who:
			imgname = "zume"
			center = F(100, h)
		else:
			imgname = "simon"
			center = F(854 - 100, h)
		img.draw(imgname, center, radius = F(80), fstretch = fstretch, angle = angle)

def showtip(tip):
	pass

