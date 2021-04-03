import pygame, math
from . import pview, ptext
from . import view, graphics, settings, state, levels, sound
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
		"zoomin": ((1230, 170), 40),
		"zoomout": ((1230, 260), 40),
		"music": ((1220, 360), 50),
		"speed": ((1220, 470), 50),
		"help": ((1180, 620), 90),
#		"pause": ((1280 - 70, 70), 60),
#		"arrows": ((1280 - 60, 430), 50),
#		"meter": ((1280 - 60, 540), 50),
	}
	selected = None
	pointed = None

tracer = None

def reset():
	global tracer
	tracer = None
	self.selected = None
	self.pointed = None

def unlocked(bname):
	if settings.DEBUG:
		return True
	if bname in ["help", "speed", "music", "zoomin", "zoomout"]:
		return True
	if bname in ["oak", "pine", "beech"]:
		if state.currentlevel in levels.buttons:
			return bname in levels.buttons[state.currentlevel]
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
	global arrows, meter
	self.pointed = buttonat(cstate.mposV)
	if not self.pointed: return
	if "click" in cstate.events:
		if self.pointed == "arrows":
			arrows = not arrows
			sound.playsound("click")
		elif self.pointed == "meter":
			meter = not meter
			sound.playsound("click")
		elif self.pointed == "speed":
			speeds = [s for s in settings.speeds if s > settings.speed]
			settings.speed = min(speeds or settings.speeds)
			sound.playsound("click")
		elif self.pointed == "music":
			tracks = [None, 0, 1, 2, 3]
			sound.playmusic(tracks[(tracks.index(settings.mtrack) + 1) % len(tracks)])
			sound.playsound("click")
		elif self.pointed == "zoomin":
			z0 = view.cameraz
			view.zoom(1)
			sound.playsound("no" if z0 == view.cameraz else "click")
		elif self.pointed == "zoomout":
			z0 = view.cameraz
			view.zoom(-1)
			sound.playsound("no" if z0 == view.cameraz else "click")
		elif self.selected == self.pointed:
			self.selected = None
			sound.playsound("unclick")
		else:
			self.selected = self.pointed
			sound.playsound("click")

def draw():
#	pview.screen.fill((30, 30, 60), T(self.rect))
	for j, (bname, (bpos, br)) in enumerate(sorted(self.buttons.items())):
		if not unlocked(bname):
			continue
		if bname == self.pointed:
			cmask = None
		else:
			cmask = 160, 160, 160, 255
		if bname in ["beech", "oak", "pine"]:
			graphics.drawimg(tuple(T(bpos)), bname, scale = 0.0025 * T(br), cmask = cmask)
		elif bname in ["pause", "help"]:
			graphics.drawimg(tuple(T(bpos)), "shroom-0", scale = 0.005 * T(br), angle = j * 360 * math.phi, cmask = cmask)
		elif bname in ["arrows", "meter", "speed", "music", "zoomin", "zoomout"]:
			graphics.drawimg(tuple(T(bpos)), "shroom-1", scale = 0.005 * T(br), angle = j * 360 * math.phi, cmask = cmask)
		else:
			pygame.draw.circle(pview.screen, (50, 50, 100), T(bpos), T(br))
		f = 3 if bname == self.pointed else 2.7
		if bname == "arrows":
			text = "Arrows\n%s" % ("On" if arrows else "Off")
		elif bname == "meter":
			text = "Meter\n%s" % ("On" if meter else "Off")
		elif bname == "speed":
			text = ("%.1fx" if settings.speed != int(settings.speed) else "%dx") % settings.speed
		elif bname == "music":
			text = "Music\nOff" if settings.mtrack is None else "Track\n#%d" % (settings.mtrack + 1)
		elif bname == "help":
			text = "Help &\nSettings"
		elif bname == "zoomin":
			text = " + "
		elif bname == "zoomout":
			text = " - "
		else:
			text = bname.upper()
		fontsize = T(f * br / max(max(len(line) for line in text.splitlines()), 1))
		color = (255, 255, 255) if bname == self.selected else (200, 200, 255)
		ptext.draw(text, center = T(bpos), fontsize = fontsize, color = color,
			owidth = 1, shade = 1)

def selected():
	return self.selected

