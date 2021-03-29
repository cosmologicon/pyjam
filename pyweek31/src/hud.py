import pygame
from . import pview, ptext
from . import view
from .pview import T

class self:
	rect = pygame.Rect((0, 0, 180, 720))
	buttons = {
		"maple": ((90, 100), 60),
		"oak": ((90, 240), 60),
		"ring": ((90, 400), 60),
	}
	selected = None

def contains(pV):
	return T(self.rect).collidepoint(pV)

def control(mposV, events):
	if not contains(mposV):
		return
	if "click" in events:
		for bname, (bpos, br) in self.buttons.items():
			if view.distance(mposV, T(bpos)) < T(br):
				if bname == "ring":
					if self.selected == "ring0":
						self.selected = "ring1"
					elif self.selected == "ring1":
						self.selected = "ring2"
					else:
						self.selected = "ring0"
				else:
					self.selected = bname
				break
		else:
			self.selected = None

def draw():
	pview.screen.fill((30, 30, 60), T(self.rect))
	for bname, (bpos, br) in self.buttons.items():
		pygame.draw.circle(pview.screen, (50, 50, 100), T(bpos), T(br))
		ptext.draw(bname, center = T(bpos), fontsize = T(30))

def selected():
	return self.selected

