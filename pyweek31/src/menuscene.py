import math
import pygame
from . import ptext, pview, state, progress, levels, graphics, settings
from . import scene
from .pview import T

class self:
	pointed = None

buttons = {
	levelname: ((200 + 100 * j, 400 + j % 2 * 200), 100)
	for j, levelname in enumerate(levels.data)
}

def control(cstate):
	self.pointed = None
	for bname, (bpos, br) in buttons.items():
		if bname in progress.unlocked and math.distance(cstate.mposV, T(bpos)) < T(br):
			self.pointed = bname
			if "click" in cstate.events:
				goto(bname)
	if "quit" in cstate.kdowns:
		scene.pop()

def goto(levelname):
	from . import scene, playscene
	state.currentlevel = levelname
	scene.push(playscene)
	playscene.init()

def think(dt):
	pass


def draw():
	pview.screen.fill((30, 30, 60))
	ptext.draw(settings.gamename, midtop = T(640, 30), fontsize = T(120), color = "green",
		shade = 1, owidth = 1)
	ptext.draw("by Christopher Night\nTeam Universe Factory\nPyWeek 31",
		midtop = T(1100, 200), fontsize = T(30), color = (50, 150, 50), shade = 1, owidth = 1,
		fontname = "Londrina")
	ptext.draw("F10: resize\nF11: fullscreen",
		bottomleft = T(10, 710), fontsize = T(30), color = (50, 150, 50), shade = 1, owidth = 1,
		fontname = "Londrina")
	for bname, (bpos, br) in buttons.items():
		if bname in progress.unlocked:
			scale = pview.f * br / 300
			cmask = (255, 255, 255, 255) if bname == self.pointed else (200, 200, 200, 255)
			if bname in progress.beaten:
				cmask = math.imix(cmask, (0, 0, 0, 255), 0.5)
			graphics.drawimg(T(bpos), "copse", scale = scale, cmask = cmask)
#			pygame.draw.circle(pview.screen, (50, 50, 100), T(bpos), T(br))
			ptext.draw(bname, center = T(bpos), fontsize = T(0.5 * br), owidth = 1, shade = 1)

