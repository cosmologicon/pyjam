import pygame
from pygame.locals import *
from . import ptext, view, scene, settings, background, sound, state
from .util import F

class self:
	pass

def init():
	self.texts = [
		"Continue from last save",
		"New game (delete save)",
		"Quit",
	]
	self.t = 0
	self.opt = 0
	sound.mplay(1)
	
def think(dt, kdowns, kpressed):
	self.t += dt
	if self.t > 1.5:
		if self.opt < len(self.texts) - 1:
			if settings.isdown("right", kdowns) or settings.isdown("down", kdowns):
				self.opt += 1
		if self.opt > 0:
			if settings.isdown("left", kdowns) or settings.isdown("up", kdowns):
				self.opt -= 1
		if settings.isdown("action", kdowns):
			end()

def end():
	from . import playscene
	scene.pop()
	if self.opt == 0:
		state.loadandrun()
	elif self.opt == 1:
		state.deleteprogress()
		state.reset()
		state.loadandrun()
	elif self.opt == 2:
		scene.quit()

def draw():
	background.drawfly()
	if settings.portrait:
		ptext.draw(settings.gamename, midtop = F(240, 10), width = F(400),
			fontsize = F(40), shadow = (1, 1), fontname = "Bungee")
	else:
		ptext.draw(settings.gamename, midtop = F(427, 10),
			fontsize = F(40), shadow = (1, 1), fontname = "Bungee")
	for jtext, text in enumerate(self.texts):
		flash = jtext == self.opt and self.t % 0.5 < 0.3
		ocolor = (255, 255, 100) if flash else (200, 200, 0)
		fcolor = (80, 80, 80) if flash else (40, 40, 40)
		rect = pygame.Rect(0, 0, 400, 80)
		rect.center = (240, 400 + 100 * jtext) if settings.portrait else (427, 150 + 100 * jtext)
		if self.t < 1.5:
			rect.y += 400 * (1.5 - self.t) ** 2
		view.screen.fill(ocolor, F(rect))
		rect.inflate_ip(-6, -6)
		view.screen.fill(fcolor, F(rect))
		ptext.draw(text, center = F(rect.center), fontsize = F(26), fontname = "Bungee",
			color = (60, 255, 255), shadow = (1, 1))


