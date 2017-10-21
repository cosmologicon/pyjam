import pygame, math
from . import state, view, mist, ptext, drawyou, settings, scene, playscene, pview
from .pview import T

class self:
	pass

def init():
	self.t = 0
	self.ending = False
	self.tend = 0
	self.choice = 0

	state.reset()
	view.reset()
	mist.init()


def think(dt, kdowns, kpressed):
	self.t += dt
	view.X0 += settings.speed * dt
	if self.ending:
		self.tend += dt
	if self.tend > 1:
		scene.set(playscene)
	if not self.ending and settings.isdown(kdowns, "select"):
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

	frun = self.t * 2 % 1
	ptext.draw(settings.gamename, T(30, 40), fontsize = T(100), color = "yellow", gcolor = "orange",
		shadow = (1, 1))
	ptext.draw("by Christopher Night", T(260, 120), fontsize = T(50), color = "yellow", gcolor = "orange",
		shadow = (1, 1))

	ptext.draw("Story Mode", T(400, 240), fontsize = T(80), color = "yellow", gcolor = "orange",
		shadow = (1, 1))
	ptext.draw("Endless Mode", T(400, 340), fontsize = T(80), color = "yellow", gcolor = "orange",
		shadow = (1, 1))

	p = T(340, 320 + 100 * self.choice)
	drawyou.running(p, T(16), frun)

	if self.t < 1:
		# TODO: add to maff
		#a = math.fadebetween((0, 255), (1, 0), self.t)
		a = math.clamp(int(255 * (1 - math.smoothfade(self.t, 0, 1))), 0, 255)
		pview.fill((255, 255, 255, a))
	if self.tend > 0:
		a = math.clamp(int(255 * math.smoothfade(self.tend, 0, 1)), 0, 255)
		pview.fill((255, 255, 255, a))

