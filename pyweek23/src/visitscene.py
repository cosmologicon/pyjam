import pygame
from pygame.locals import *
from . import ptext, view, scene, settings, image, util, background
from .util import F

class self:
	pass

def init(name):
	self.name = name
	self.texts = [
		"Sure thing.",
		"I'm sorry, I need all I can get.",
	]
	self.subtexts = [
		"You will lose half your health",
		"You will keep your current health",
	]
	self.info = "\n\n".join([
		"Finally! I thought I'd never see another human being again.",
		"I'm a crew member on board the USS Orinoco. Our ship was destroyed, but most of us made it out in these escape capsules. Damn, I still can hear Captain Sisko's order to abandon ship....",
		"Look, I've taken heavy damage. I haven't got enough hull charge to last the rest of the way back. If you're willing to transfer some of your charge over to me, I should be able to make it. If not.... Well what do you say?",
	])
	self.brank = "First Officer"
	self.bname = "Kira Nerys"

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
#	view.screen.fill((0, 40, 100))
	background.drawfly()
#	ptext.draw("Visiting: " + self.name, midtop = F(427, 10),
#		fontsize = F(40), shadow = (1, 1))
	ptext.draw(self.info, topright = F(680, 30), width = F(540), fontsize = F(24),
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
	image.Bdraw("bio-0", (760, 100), a = util.clamp(self.t * 3 - 0.3, 0, 1))
	if self.t >= 1.5:
		ptext.draw(self.brank, midtop = F(760, 170), fontsize = F(28))
		ptext.draw(self.bname, midtop = F(760, 192), fontsize = F(28))


	


