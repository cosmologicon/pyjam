import pygame, math
from . import pview, ptext
from . import view, graphics
from .pview import T

class self:
	rect = pygame.Rect((0, 0, 180, 720))
	buttons = {
		"oak": ((90, 90), 80),
		"beech": ((80, 250), 70),
		"elm": ((70, 390), 60),
		"r0-1": ((30, 360), 30),
		"r1-1": ((90, 360), 30),
		"r2-1": ((150, 360), 30),
		"s0-0": ((30, 420), 30),
		"s1-0": ((90, 420), 30),
		"s2-0": ((150, 420), 30),
		"multi": ((30, 560), 30),
		"tri": ((90, 560), 30),
		"pause": ((1230, 50), 40),
		"help": ((1230, 670), 40),
	}
	selected = None

def contains(pV):
	for bname, (bpos, br) in self.buttons.items():
		if math.distance(pV, T(bpos)) < T(br):
			return True
	return False
	return T(self.rect).collidepoint(pV)

def control(cstate):
	if not contains(cstate.mposV):
		return
	if "click" in cstate.events:
		for bname, (bpos, br) in self.buttons.items():
			if math.distance(cstate.mposV, T(bpos)) < T(br):
				self.selected = bname
				break
		else:
			self.selected = None

def draw():
#	pview.screen.fill((30, 30, 60), T(self.rect))
	for bname, (bpos, br) in self.buttons.items():
		if bname in ["beech", "oak"]:
			graphics.drawimg(tuple(T(bpos)), bname, scale = 0.0025 * T(br))
		else:
			pygame.draw.circle(pview.screen, (50, 50, 100), T(bpos), T(br))
		fontsize = T(4 * br / len(bname))
		ptext.draw(bname.upper(), center = T(bpos), fontsize = fontsize, color = (240, 240, 80),
			owidth = 0.5, ocolor = (100, 50, 0), shade = 1)

def selected():
	return self.selected

