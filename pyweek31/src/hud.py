import pygame, math
from . import pview, ptext
from . import view, graphics, settings
from .pview import T

class self:
	rect = pygame.Rect((0, 0, 180, 720))
	buttons = {
		"oak": ((90, 90), 80),
		"beech": ((80, 250), 70),
		"pine": ((70, 390), 60),
		"r0-1": ((30, 560), 30),
		"r1-1": ((90, 560), 30),
		"r2-1": ((150, 560), 30),
		"s0-0": ((30, 620), 30),
		"s1-0": ((90, 620), 30),
		"s2-0": ((150, 620), 30),
		"multi": ((30, 700), 30),
		"tri": ((90, 700), 30),
		"pause": ((1280 - 70, 70), 60),
		"help": ((1280 - 70, 720 - 70), 60),
	}
	selected = None
	pointed = None

def unlocked(bname):
	if settings.DEBUG:
		return True
	if bname in ["pause", "help"]:
		return True
	if bname in ["oak", "pine", "beech"]:
		return True
	return False

def buttonat(pV):
	for bname, (bpos, br) in self.buttons.items():
		if math.distance(pV, T(bpos)) < T(br) and unlocked(bname):
			return bname
	return None
	

def contains(pV):
	return buttonat(pV) is not None

def control(cstate):
	self.pointed = buttonat(cstate.mposV)
	if not self.pointed: return
	if "click" in cstate.events:
		self.selected = buttonat(cstate.mposV)

def draw():
#	pview.screen.fill((30, 30, 60), T(self.rect))
	for bname, (bpos, br) in self.buttons.items():
		if not unlocked(bname):
			continue
		if bname == self.pointed:
			cmask = None
		else:
			cmask = 160, 160, 160, 255
		if bname in ["beech", "oak", "pine"]:
			graphics.drawimg(tuple(T(bpos)), bname, scale = 0.0025 * T(br), cmask = cmask)
		elif bname in ["pause", "help"]:
			graphics.drawimg(tuple(T(bpos)), "shroom-0", scale = 0.005 * T(br), cmask = cmask)
		else:
			pygame.draw.circle(pview.screen, (50, 50, 100), T(bpos), T(br))
		f = 3.6 if bname == self.pointed else 2.7
		fontsize = T(f * br / max(len(bname), 5))
		ptext.draw(bname.upper(), center = T(bpos), fontsize = fontsize, color = (255, 255, 128),
			owidth = 1, ocolor = (100, 50, 0), shade = 1)

def selected():
	return self.selected

