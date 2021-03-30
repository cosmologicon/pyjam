import pygame, math
from . import pview, ptext
from . import view
from .pview import T

class self:
	rect = pygame.Rect((0, 0, 180, 720))
	buttons = {
		"maple": ((45, 100), 40),
		"oak": ((45, 240), 40),
		"r0-1": ((30, 360), 30),
		"r1-1": ((90, 360), 30),
		"r2-1": ((150, 360), 30),
		"s0-0": ((30, 420), 30),
		"s1-0": ((90, 420), 30),
		"s2-0": ((150, 420), 30),
		"rot": ((90, 480), 30),
		"multi0": ((30, 560), 30),
		"tri0": ((90, 560), 30),
		"tri1": ((150, 560), 30),
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
				if bname == "rot":
					if self.selected[:-1] in ("s0-", "s1-", "s2-", "multi"):
						j = (int(self.selected[-1]) + 1) % 6
						self.selected = self.selected[:-1] + str(j)
					if self.selected[:-1] in ("r0-", "r1-", "r2-"):
						j = (int(self.selected[-1]) + 1) % 4
						self.selected = self.selected[:-1] + str(j)
				else:
					self.selected = bname
				break
		else:
			self.selected = None

def draw():
#	pview.screen.fill((30, 30, 60), T(self.rect))
	for bname, (bpos, br) in self.buttons.items():
		pygame.draw.circle(pview.screen, (50, 50, 100), T(bpos), T(br))
		ptext.draw(bname, center = T(bpos), fontsize = T(30))

def selected():
	return self.selected

