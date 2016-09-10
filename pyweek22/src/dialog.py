import pygame, math, os.path
from . import ptext, progress, img, sound
from .util import F

lines = {}
for line in open(os.path.join("data", "transcript.txt")):
	if not line:
		continue
	filename, who, line = line.split(" ", 2)
	convo = filename[:3]
	if convo not in lines:
		lines[convo] = []
	lines[convo].append((filename, who, line.rstrip()))

queue = []
playing = None
tquiet = 0
tbreath = 0
currenttip = None

def quiet():
	return not playing and not queue

def play(dname):
	if dname in progress.heard:
		return
	progress.heard.add(dname)
	progress.save()
	queue.extend(lines[dname])

def think(dt):
	global tquiet, playing, tplaying, tbreath
	if quiet():
		tquiet += dt
	else:
		tquiet = 0
	if queue and not playing:
		tplaying = 0
		tbreath += dt
		if tbreath > 0.15:
			playing = queue.pop(0)
			filename, who, line = playing
			channel = pygame.mixer.Channel(1)
			channel.play(sound.getsound(filename, "dialog"))
	if playing:
		tplaying += dt
		tbreath = 0
		if channelfree():
			playing = None

def draw():
	if playing:
		filename, who, line = playing
		t = pygame.time.get_ticks() * 0.001
		h, angle, fstretch = 390, 0, 1
		if "bounce" in who:
			freq = float(who[7:])
			h = 400 - 20 * abs(math.sin(freq * math.tau * t))
		if "rock" in who:
			freq = float(who[5:])
			angle = 10 * math.sin(freq * math.tau * t)
		if "sink" in who:
			h += 20 * math.sqrt(tplaying)
		if "Z" in who:
			imgname = "zume"
			center = F(100, h)
			align = "right"
		else:
			imgname = "simon"
			center = F(854 - 100, h)
			align = "left"
		alpha = math.clamp(4 * tplaying, 0, 1)
		ptext.draw(line, midbottom = F(854 / 2, 470), width = F(500),
			color = (255, 100, 255), shadow = (1, 1),
			fontsize = F(36), fontname = "PatrickHand")
		img.draw(imgname, center, radius = F(80), fstretch = fstretch, angle = angle, tocache = False)

	if currenttip:
		ptext.draw(currenttip, center = F(854 / 2, 160), width = F(500),
			color = (255, 255, 100), shadow = (1, 1), fontname = "PermanentMarker",
			fontsize = F(28))

def channelfree():
	channel = pygame.mixer.Channel(1)
	return not channel.get_busy()

def showtip(tip):
	global currenttip
	currenttip = tip

def abort():
	skip()
	del queue[:]

def skip():
	global playing
	channel = pygame.mixer.Channel(1)
	channel.stop()
	playing = None
	

if __name__ == "__main__":
	from . import mhack, view
	ptext.FONT_NAME_TEMPLATE = "data/font/%s.ttf"
	pygame.init()
	toplay = sorted(lines)
	view.screen = pygame.display.set_mode((854, 480))
	clock = pygame.time.Clock()
	while True:
		dt = 0.001 * clock.tick()
		for e in pygame.event.get():
			if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				exit()
			if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
				skip()
			if e.type == pygame.KEYDOWN and e.key == pygame.K_TAB:
				abort()
		if tquiet > 1:
			if toplay:
				play(toplay.pop(0))
			else:
				exit()
		view.screen.fill((0, 50, 50))
		think(dt)
		draw()
		pygame.display.flip()

