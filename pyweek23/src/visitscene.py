import pygame
from pygame.locals import *
from . import ptext, view, scene, settings
from .util import F

class self:
	pass

def init(name):
	self.name = name
	self.texts = [
		"Sure thing.",
		"I'm sorry, I really need the fuel myself.",
	]
	self.subtexts = [
		"You will lose half your health",
		"You will keep your current health",
	]
	self.info = "\n".join([
		"Finally, someone! I thought I'd never see another human being again.",
		"I'm one of professor Cortadora's team. Since the accident on the spaceship I managed to survive on this planet. Damn, I still can hear the emergency signal.",
		"Luckily I was able to get one of these capsules. And if YOU could transfer some fuel to it, I could make my way back home. Would you be so kind?",
	])

	self.t = 0
	self.opt = 0
	
def think(dt, kdowns, kpressed):
	self.t += dt
	if self.t > 1.5:
		if self.opt == 0:
			if settings.isdown("right", kdowns) or settings.isdown("down", kdowns):
				self.opt = 1
		elif self.opt == 1:
			if settings.isdown("left", kdowns) or settings.isdown("up", kdowns):
				self.opt = 0
		if settings.isdown("action", kdowns):
			scene.pop()

def draw():
	view.screen.fill((0, 40, 100))
	ptext.draw("Visiting: " + self.name, midtop = F(427, 10),
		fontsize = F(40), shadow = (1, 1))
	ptext.draw(self.info, topright = F(760, 50), width = F(600), fontsize = F(24),
		color = "turquoise", shadow = (1, 1))
	y0 = 260 if self.t > 1.5 else 260 + 400 * (1.5 - self.t) ** 2
	for jtext, (text, subtext) in enumerate(zip(self.texts, self.subtexts)):
		flash = jtext == self.opt and self.t % 0.5 < 0.3
		ocolor = (255, 255, 100) if flash else (200, 200, 0)
		fcolor = (80, 80, 80) if flash else (40, 40, 40)
		view.screen.fill(ocolor, F(150, y0, 554, 90))
		view.screen.fill(fcolor, F(153, y0 + 3, 548, 84))
		ptext.draw(text, topleft = F(180, y0 + 10), fontsize = F(48),
			color = (60, 255, 255), shadow = (1, 1))
		ptext.draw(subtext, topleft = F(280, y0 + 52), fontsize = F(28),
			color = (0, 180, 180), shadow = (1, 1))
		y0 += 100


