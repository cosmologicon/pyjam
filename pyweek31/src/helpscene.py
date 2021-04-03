import math
import pygame
from . import ptext, pview, scene, settings, sound, state, graphics
from .pview import T

class self:
	pointed = None

buttons = {
	"sound": ((70, 650), 50),
	"music": ((180, 650), 50),
	"silence": ((290, 650), 50),

	"arrows": ((490, 650), 50),
	"meter": ((590, 650), 50),
	"shade": ((690, 650), 50),
	"trails": ((790, 650), 50),

	"back": ((990, 650), 50),
	"menu": ((1100, 650), 50),
	"quit": ((1210, 650), 50),

}

def getbtext(bname):
	if bname == "sound":
		return "SFX\n%d%%" % settings.soundvolume
	if bname == "music":
		return "Music\n%d%%" % settings.musicvolume
	if bname == "silence":
		return "Silence"
	if bname == "arrows":
		return "Arrows\n%s" % ("On" if settings.showarrows else "Off")
	if bname == "meter":
		return "Meter\n%s" % ("On" if settings.showmeter else "Off")
	if bname == "shade":
		return "Shade\nFX\n%s" % ({0: "Off", 1: "Low", 3: "On"}.get(settings.nshade, "??"))
	if bname == "trails":
		return "Trail\nFX\n%s" % ("On" if settings.trails else "Off")
	if bname == "silence":
		return "Silence"
	if bname == "back":
		return "Resume\nGame"
	if bname == "menu":
		return "Menu\n(restart\nlevel)"
	if bname == "quit":
		return "Quit\n(save\nprogress)"

def unlocked(bname):
	if bname in ["quit"]:
		return True
	return bname in progress.unlocked

def control(cstate):
	self.pointed = None
	for bname, (bpos, br) in buttons.items():
		if math.distance(cstate.mposV, T(bpos)) < T(br):
			self.pointed = bname
			if "click" in cstate.events:
				click(bname)

def click(bname):
	sound.playsound("click")
	if bname == "arrows":
		settings.showarrows = not settings.showarrows
	elif bname == "meter":
		settings.showmeter = not settings.showmeter
	elif bname == "shade":
		settings.nshade = 1 if settings.nshade == 0 else 0 if settings.nshade == 3 else 3
	elif bname == "trails":
		settings.trails = not settings.trails
	elif bname == "music":
		vs = settings.vlevels
		settings.musicvolume = vs[(vs.index(settings.musicvolume) + 1) % len(vs)]
		sound.updatemusicvolume()
	elif bname == "sound":
		vs = settings.vlevels
		settings.soundvolume = vs[(vs.index(settings.soundvolume) + 1) % len(vs)]
	elif bname == "silence":
		settings.musicvolume = 0
		settings.soundvolume = 0
		sound.updatemusicvolume()
	elif bname == "back":
		scene.pop()
	elif bname == "menu":
		scene.pop()
		scene.pop()
		state.reset()
	elif bname == "quit":
		scene.pop()
		scene.pop()
		scene.pop()

def think(dt):
	pass

def draw():
	from . import playscene
	playscene.draw()
	pview.fill((40, 40, 40, 240))
	text = "\n".join([
		"Goal: plant trees to direct the magical energy from the flowers to the toadstool rings.",
		"Each ring requires 3 streams of energy whose color matches the toadstools.",
		"Activate all rings at the same time to complete the level.",
		"Energy of the wrong color will prevent a ring from activating.",
		"Oak tree: shift energy one hex to the right (or left) without changing its direction.",
		"Beech tree: change energy direction by 60 degrees to the right (or left).",
		"Pine tree: change energy direction by 120 degrees to the right (or left).",
	])
	ptext.draw(text, topleft = T(60, 50), fontsize = T(26), width = T(560), fontname = "Londrina",
		color = (200, 200, 255), shade = 0.5, shadow = (1, 1), pspace = 0.5)
	text = "\n".join([
		"Left click: plant tree",
		"Left click on tree: swap orientation",
		"Left click on flower: highlight energy from this flower (click again to disable)",
		"Right click on tree: remove tree",
		"Scroll wheel: zoom",
		"F10: cycle resolutions",
		"F11: fullscreen",
		"F12: screenshot",
		"See README.txt for command line options and settings.",
	])

	ptext.draw(text, topleft = T(660, 50), fontsize = T(26), width = T(560), fontname = "Londrina",
		color = (200, 200, 255), shade = 0.5, shadow = (1, 1), pspace = 0.5)
	for j, (bname, (bpos, br)) in enumerate(sorted(buttons.items())):
		scale = pview.f * br / 200
		cmask = (255, 255, 255, 255) if bname == self.pointed else (200, 200, 200, 255)
		graphics.drawimg(T(bpos), "shroom-1", scale = scale, cmask = cmask, angle = 360 * math.phi * j)
		fontsize = T(0.5 * br * (1.1 if bname == self.pointed else 1))
		ptext.draw(getbtext(bname),	center = T(bpos),
			fontsize = fontsize, owidth = 1, shade = 1)


