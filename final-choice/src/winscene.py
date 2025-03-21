import math, random, pygame
from pygame.locals import *
from . import state, thing, background, settings, hud, util, sound, image, ptext, scene, creditsscene
from .pview import T

class self:
	pass

def init():
	dname = "B" if not state.good else "D" if not state.best else "E"
	self.spawner = sound.Dplayer(dname)
	self.t = 0
	self.popped = False
	sound.mplay(2)
	state.mupdate()
	state.removequicksave()
	state.deleteprogress()

def think(dt, kdowns, kpressed):
	if self.popped:
		return
	self.t += dt
	if self.t >= 2:
		self.spawner.think(dt)
		if not self.spawner.alive:
			self.popped = True
			scene.pop()
			if state.good:
				scene.push(creditsscene)

def draw():
	background.drawfly()
	self.spawner.draw()

	title = "Bad ending" if not state.good else "Good ending" if not state.best else "Best ending"

	pos = T(240, 240) if settings.portrait else T(427, 140)
	ptext.draw("Thank you for playing", midbottom = pos, fontname = "Bungee", fontsize = T(40),
		color = (200, 255, 255), width = T(400 if settings.portrait else 700))
	pos = T(240, 260) if settings.portrait else T(427, 160)
	ptext.draw(title, midtop = pos, fontname = "Bungee", fontsize = T(32),
		color = (100, 255, 255))

	for j, name in enumerate("123456X7CJ"):
		dx = 80 * (j % 5)
		dy = 80 * (j // 5)
		pos = (76 + dx, 400 + dy) if settings.portrait else (264 + dx, 260 + dy)
		a = util.clamp((self.t - 2) * 2, 0, 1 if name in state.met else 0.99)
		if a:
			image.Bdraw("bio-" + name, pos, 60, a)
		alpha = util.clamp((self.t - 3) * 2, 0, 1)
		if alpha:
			if name == "7":
				pass
			elif name not in state.met:
				ptext.draw("?", center = T(pos), fontsize = T(50), fontname = "PermanentMarker",
					color = "red", owidth = 1, alpha = alpha)
			elif name not in state.saved:
				ptext.draw("X", center = T(pos), fontsize = T(50), fontname = "PermanentMarker",
					color = "red", owidth = 1, alpha = alpha)


