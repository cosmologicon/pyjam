import pygame, math, numpy
from . import scene, pview, ptext, progress
from . import draw as D
from .pview import T

lines = {
	"tutorial2": [
		"V My good lady! How do you do?",
		"Y Oh my, are you a fellow butterfly lover?",
		"V In a manner of speaking. My name is Professor Dame Victoria Winger.",
		"V I am the Chair of the Department of Mothematics at Eldbridge University.",
		"Y Goodness me! I'm Miranda Flutterbie. A pleasure to make your acquaintance!",
		"V Would you permit me to observe for a few moments?",
		"Y Certainly! It'll be good to have some company!",
	],
	"tutorial3": [
		"V Incredible! Just as I suspected!",
		"V Miranda, have you ever heard of the Butterfly Effect?",
		"Y I'm afraid not. Should I have?",
		"V It's a theory of lepidoptery that I've been studying for years,",
		"V but sadly, nobody has ever found any proof it actually exists.",
		"V Watching you play that last level, however, I'm convinced it's real!",
	],
	"tutorial3-post": [
		"Y So just what is this 'Butterfly Effect', Victoria?",
		"V I'll explain everything, but please come with me to the Ministry of Insects.",
		"V They must be informed of this!",
	],
}


class self:
	pass


def init(track):
	self.track = track
	self.jline = -1
	self.t = 0
	self.tline = 0
	self.a = 0
	self.switching = True
	self.ready = False

	if track in lines and track not in progress.dseen:
		self.lines = list(lines[track])
		progress.dseen.add(track)
		drawwho("Y", -1, 1)
		drawwho("E", 1, 1)
		drawwho("V", 1, 1)
	if track not in lines:
		scene.pop()
		self.lines = []

def control(keys):
	if "act" in keys and not self.switching:
		self.switching = True
		self.ready = False
	if "forfeit" in keys:
		self.jline = len(self.lines)

def think(dt):
	if not self.switching:
		D.killtime(0.02)
	if self.ready:
		self.t += dt
	if self.switching:
		self.tline = 0
		self.a = math.approach(self.a, 1, 3.5 * dt)
		if self.a == 1:
			self.switching = False
			self.a = 0
			self.jline += 1
			if self.jline == len(self.lines):
				scene.pop()
	else:
		self.tline += dt
	if not self.switching and 0 <= self.jline < len(self.lines):
		t = 1 + 0.08 * len(self.lines[self.jline])
		if self.tline > t:
			self.switching = True
			self.ready = False

def layout(jline):
	if not 0 <= jline < len(self.lines):
		color = 0, 0, 0
		line = None
		who = None
		dpos = 0
	else:
		who, _, line = self.lines[jline].partition(" ")
		color = {
			"Y": (0, 255, 255),
			"E": (255, 200, 100),
			"V": (255, 0, 255),
		}[who]
		dpos = -1 if who == "Y" else 1
	return line, who, dpos, color

def drawback(color, dpos):
	w, h = pview.size
	w //= 8
	h //= 8
	xs = numpy.arange(float(w)).reshape([w, 1, 1]) / w - 0.5
	ys = numpy.arange(float(h)).reshape([1, h, 1]) / h - 0.5
	ys = ys / (1.0 - 1.4 * dpos * xs)
	t = 0.001 * pygame.time.get_ticks()
	f = 0.25 + sum([
		0.06 * numpy.sin(20 * ys + 4 * t),
		0.05 * numpy.sin(30 * ys - 7 * t),
		0.04 * numpy.sin(43 * ys - 10 * t),
		0.03 * numpy.sin(55 * ys + 13 * t),
	])
	img = pygame.Surface((w, h)).convert()
	img.fill(color)
	arr = pygame.surfarray.pixels3d(img)
	arr[:,:,:] = (arr * f).astype(arr.dtype)
	del arr
	pview.screen.blit(pygame.transform.smoothscale(img, pview.size), (0, 0))
	
def drawwho(who, dpos, a):
	if who == "Y":
		x = 640 + dpos * (400 + 600 * a)
		D.drawimg("you", T(x, 400), T(1400))
	elif who == "E":
		x = 640 + dpos * (360 + 600 * a)
		D.drawimg("elmer", T(x, 400), T(1600))
	elif who == "V":
		x = 640 + dpos * (360 + 600 * a)
		D.drawimg("victoria", T(x, 400), T(1400))
	

def drawline(line, who, color, dpos, a):
	fontname = {
		"Y": "ChangaOne",
		"E": "ChangaOne",
		"V": "ChangaOne",
	}[who]
	ptext.draw(line, center = T(640 + (100 + 1200 * a) * dpos, 600), width = T(960),
		color = color, shade = 1, shadow = (1, 1.3), owidth = 0.25,
		fontsize = T(60), fontname = fontname)

def draw():
	self.ready = True
	line, who, dpos, color = layout(self.jline)
	if not self.switching:
		drawback(color, dpos)
		if who:
			drawwho(who, dpos, 0)
		if line:
			drawline(line, who, color, dpos, 0)
	else:
		line1, who1, dpos1, color1 = layout(self.jline + 1)
		acolor = math.imix(color, color1, self.a)
		drawback(acolor, math.mix(dpos, dpos1, self.a))
		if who and who1 and who == who1:
			drawwho(who, dpos, 0)
		else:
			if who:
				drawwho(who, dpos, self.a)
			if who1:
				drawwho(who1, dpos1, 1 - self.a)
		if line:
			drawline(line, who, color, dpos, self.a)
		if line1:
			drawline(line1, who1, color1, dpos1, 1 - self.a)
	ptext.draw("Space: next   Backspace: skip", fontname = "ChangaOne", color = (255, 220, 200),
		fontsize = T(18), bottomright = T(1270, 710),  shade = 1, owidth = 0.5, shadow = (1, 1))


