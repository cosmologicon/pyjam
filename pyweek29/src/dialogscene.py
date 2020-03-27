import pygame, math, numpy
from . import scene, pview, ptext, progress
from . import draw as D
from .pview import T

lines = {
	"tutorial1": [
		"Y Lepidoptery?",
		"Y Don't mind if I do!",
		"V Wait for me!",
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

def think(dt):
	t = pygame.time.get_ticks()
	if not self.switching:
		D.killtime(0.02)
	print(pygame.time.get_ticks() - t)
	if self.ready:
		self.t += dt
		self.tline += dt
	if self.switching:
		self.a = math.approach(self.a, 1, 5 * dt)
		if self.a == 1:
			self.switching = False
			self.a = 0
			self.jline += 1
			if self.jline == len(self.lines):
				scene.pop()

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
		D.you("standing", T(x, 800), T(1600), 0, True)
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
	ptext.draw(line, center = T(640 + (100 + 1200 * a) * dpos, 600), width = T(720), color = color,
		shade = 1, shadow = (1, 1.3), owidth = 0.25,
		fontsize = T(120), fontname = fontname)

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
		


