import pygame, random, math
from . import pview, ptext, graphics, view
from .pview import T


Ntrial = 5

class self:
	pass

def init():
	self.t = 0
	self.mode = "intro"
	self.jstep = 0
	self.rect = None
	self.times = {
		"cal0": [],
		"cal1": [],
		"cal2": [],
		"cal3": [],
	}
	self.mode = "cal2"
	advance()

def randomrect():
	rect = pygame.Rect(0, 0, 80, 80)
	rect.center = random.randint(200, 1280 - 200), random.randint(200, 720 - 200)
	return rect

def advance():
	if self.mode == "intro":
		self.mode = "cal0"
	elif self.mode == "cal0":
		self.times["cal0"].append(self.t)
		if len(self.times["cal0"]) == Ntrial:
			self.mode = "cal1"
			print(sorted(self.times["cal0"]))
	elif self.mode == "cal1":
		self.times["cal1"].append(self.t)
		if len(self.times["cal1"]) == Ntrial:
			self.mode = "cal2"
			print(sorted(self.times["cal1"]))
	elif self.mode == "cal2":
		self.times["cal2"].append(self.t)
		if len(self.times["cal2"]) == Ntrial:
			self.mode = "cal3"
			print(sorted(self.times["cal2"]))
	elif self.mode == "cal3":
		self.times["cal3"].append(self.t)
		if len(self.times["cal3"]) == Ntrial:
			self.mode = "done"
			print(sorted(self.times["cal3"]))
	elif self.mode == "done":
		from . import scene, playscene
		scene.current = playscene
	self.t = 0
	self.rect = randomrect()
	view.xG0 = random.uniform(0, 1000)
	view.yG0 = random.uniform(0, 1000)

def misclick():
	self.t = 0
	self.rect = randomrect()
	if self.mode == "cal0":
		self.times["cal0"] = []
	if self.mode == "cal1":
		self.times["cal1"] = []
	if self.mode == "cal2":
		self.times["cal2"] = []
	if self.mode == "cal3":
		self.times["cal3"] = []

def think(dt, kdowns, kpressed, mpos, mdowns):
	self.t += dt
	if self.mode in ["intro", "done"]:
		if self.t > 0.5 and 1 in mdowns:
			advance()
	if self.mode in ["cal0", "cal1", "cal2", "cal3"]:
		if 1 in mdowns:
			if T(self.rect).collidepoint(mpos):
				advance()
			else:
				misclick()

def draw():
	if self.mode == "intro":
		pview.fill((30, 30, 30))
		text = "\n".join([
			"Click on the black box as soon as you can see it.",
			"I recommend adjusting the resolution to what you",
			"plan to play with before doing this step. (F10, F11)",
			"",
			"Click to begin.",
		])
		ptext.draw(text, center = pview.center, fontsize = T(30), owidth = 1)
	if self.mode == "done":
		pview.fill((30, 30, 30))
		text = "\n".join([
			"All done. Ready to play.",
			"",
			"Noticing the dark objects in the game is supposed to be",
			"challenging but not frustrating, but the difficulty",
			"depends a lot on your monitor setup. If you find the game",
			"too hard or too easy, see README.md to adjust the calibration.",
			"",
			"Click to begin the game.",
		])
		ptext.draw(text, center = pview.center, fontsize = T(30), owidth = 1)
	if self.mode == "cal0":
		color = [
			int(math.fuzzrange(50, 100, len(self.times["cal0"]), 15, j))
			for j in range(3)
		]
		pview.fill(color)
	if self.mode == "cal1":
		color = math.imix((0, 0, 0), (100, 100, 100), self.t * 0.01)
		pview.fill(color)
	if self.mode == "cal2":
		pview.fill((0, 0, 0))
		frac = math.interp(self.t, 0, 0.01, 100, 1)
		graphics.drawstarrange(0.03, frac)
	if self.mode == "cal3":
		pview.fill((0, 0, 0))
		graphics.drawnebula()
	if self.mode not in ["intro", "done"]:
		pview.screen.fill((0, 0, 0), T(self.rect))
	ptext.draw("Calibrating Instruments", midtop = T(640, 10),
		fontsize = T(80), owidth = 1)
	ptext.draw("F10: change resolution\nF11: toggle fullscreen", bottomleft = T(10, 710),
		fontsize = T(30), owidth = 1)

