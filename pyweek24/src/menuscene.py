import pygame, math
from . import state, view, mist, ptext, drawyou, settings, scene, playscene, pview, sound, endless
from .pview import T

class self:
	pass

def init():
	if settings.unlock:
		endless.unlock()
	self.t = 0
	self.ending = False
	self.tend = 0
	self.choice = 0

	state.reset()
	view.reset()
	mist.init()
	sound.playmusic("pamgaea")
	self.hiscore = endless.gethiscore()


def think(dt, kdowns, kpressed):
	self.t += dt
	view.X0 += settings.speed * dt
	if self.ending:
		self.tend += dt
	if self.tend > 1:
		if self.choice == 0:
			scene.set(playscene)
		else:
			scene.set(endless)
	if not self.ending and settings.isdown(kdowns, "select"):
		if self.choice == 0 or self.hiscore is not None:
			self.ending = True
	if not self.ending:
		if any(settings.isdown(kdowns, kname) for kname in ["up", "down", "left", "right"]):
			self.choice = 1 - self.choice

def draw():
	pview.fill((100, 100, 255))

	objs = list(state.effects)
	objs.sort(key = lambda obj: (obj.z, -obj.y))
	for obj in objs:
		obj.draw()

	color = (200, 150, 255)
	gcolor = (160, 80, 200)
	frun = self.t * 2 % 1
	ptext.draw(settings.gamename, T(30, 20), fontsize = T(100), color = color, gcolor = gcolor,
		shadow = (1, 1), fontname = "SpicyRice")
	ptext.draw("by Christopher Night", T(460, 140), fontsize = T(30), color = color, gcolor = gcolor,
		shadow = (1, 1), fontname = "SpicyRice")

	ptext.draw("Story Mode / Tutorial", T(300, 220), fontsize = T(70), color = color, gcolor = gcolor,
		shadow = (1, 1), fontname = "SpicyRice")

	ptext.draw("Endless Mode", T(300, 320), fontsize = T(70), color = color, gcolor = gcolor,
		shadow = (1, 1), fontname = "SpicyRice",
		alpha = 0.2 if self.hiscore is None else 1)

	ptext.draw("F10: toggle window size\nF11: toggle fullscreen\nEsc: quit",
		fontsize = T(20), color = "black",
		topright = T(1000, 20), fontname = "Acme")
	if self.hiscore is not None:
		ptext.draw("High score: %d m" % self.hiscore, midbottom = T(512, 460),
		fontsize = T(30), color = "black",
		fontname = "Acme")

	p = T(240, 320 + 100 * self.choice)
	drawyou.running(p, T(16), frun)

	if self.t < 1:
		# TODO: add to maff
		#a = math.fadebetween((0, 255), (1, 0), self.t)
		a = math.clamp(int(255 * (1 - math.smoothfade(self.t, 0, 1))), 0, 255)
		pview.fill((255, 255, 255, a))
	if self.tend > 0:
		a = math.clamp(int(255 * math.smoothfade(self.tend, 0, 1)), 0, 255)
		pview.fill((255, 255, 255, a))

