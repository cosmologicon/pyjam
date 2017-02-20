import pygame
from pygame.locals import *
from . import ptext, view, scene, settings
from .util import F

class self:
	pass

def init():
	self.texts = [
		"Continue from last save",
		"New game (delete save)",
		"Quit",
	]
	self.info = "Thank you for coming. I didn't think I would ever make it. Please get me out of here...."
	self.t = 0
	self.opt = 0
	
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
		pass
	elif self.opt == 1:
		scene.push(playscene)
	elif self.opt == 2:
		scene.quit()

def draw():
	view.screen.fill((0, 40, 100))
	ptext.draw("Game over", midtop = F(427, 10),
		fontsize = F(40), shadow = (1, 1))
	y0 = 160 if self.t > 1.5 else 160 + 400 * (1.5 - self.t) ** 2
	for jtext, text in enumerate(self.texts):
		flash = jtext == self.opt and self.t % 0.5 < 0.3
		ocolor = (255, 255, 100) if flash else (200, 200, 0)
		fcolor = (80, 80, 80) if flash else (40, 40, 40)
		view.screen.fill(ocolor, F(150, y0, 554, 90))
		view.screen.fill(fcolor, F(153, y0 + 3, 548, 84))
		ptext.draw(text, midtop = F(427, y0 + 10), fontsize = F(48),
			color = (60, 255, 255), shadow = (1, 1))
		y0 += 100


