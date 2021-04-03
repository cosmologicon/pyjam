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
buttons["quit"] = (1220, 660), 50

btext = {
	"single": "Gnicholas",
	"overage": "Gnatalie",
	"beech2": "Gnancy",
	"double": "Gneil",
	"triple": "Gnaomi",
	"pine3": "Gnicole",
	"oakpine": "Gnathan",
	"beechpine": "Gnatasha",
	"final0": "Gnorman",
	"final1": "Gnobody",
	"quit": "SAVE &\nQUIT",
}

def unlocked(bname):
	if bname in ["quit"]:
		return True
	return bname in progress.unlocked

def control(cstate):
	self.pointed = None
	for bname, (bpos, br) in buttons.items():
		if unlocked(bname) and math.distance(cstate.mposV, T(bpos)) < T(br):
			self.pointed = bname
			if "click" in cstate.events:
				if bname == "quit":
					scene.pop()
				else:
					goto(bname)
	if "quit" in cstate.kdowns:
		scene.pop()

def goto(levelname):
	from . import scene, playscene
	scene.push(playscene)
	state.setspec(levelname)
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
		if not unlocked(bname): continue
		tcolor = 255, 255, 255
		if bname == "quit":
			scale = pview.f * br / 200
			cmask = (255, 255, 255, 255) if bname == self.pointed else (200, 200, 200, 255)
			graphics.drawimg(T(bpos), "shroom-0", scale = scale, cmask = cmask)
		else:
			scale = pview.f * br / 300
			cmask = (255, 255, 255, 255) if bname == self.pointed else (200, 200, 200, 255)
			if bname in progress.beaten:
				cmask = math.imix(cmask, (0, 0, 0, 255), 0.5)
			graphics.drawimg(T(bpos), "copse", scale = scale, cmask = cmask)
			tcolor = 200, 255, 200
		fontsize = T(0.5 * br * (1.15 if bname == self.pointed else 1))
		text = btext.get(bname, bname.upper())
		ptext.draw(text, center = T(bpos), fontsize = fontsize, color = tcolor, owidth = 1, shade = 1)
		if bname in progress.beaten:
			ptext.draw("DONE", center = T(bpos[0], bpos[1] + 40), color = (200, 200, 255), fontsize = T(30), owidth = 1, shade = 1)

