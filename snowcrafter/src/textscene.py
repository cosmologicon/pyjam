from __future__ import division
import pygame, math
from . import pview, ptext, background, view, scene, sound, settings
from .pview import T, I

acceptedchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_ "

class self:
	pass

def init(box0, text, ondone):
	global ondone_
	self.box0 = box0.copy()
	self.box1 = box0.copy()
	self.box1.center = pview.center0
	self.box = box0.copy()
	self.center = self.box.center
	self.text = text
	self.ending = False
	self.done = False
	ondone_ = ondone

def think(dt, controls):
	background.update(dt)
	if self.ending:
		self.center = math.softapproach(self.center, self.box0.center, 30 * dt)
		if self.center == self.box0.center and not self.done:
			scene.pop()
			self.done = True
			ondone_(self.text)
			settings.save()
	else:
		self.center = math.softapproach(self.center, self.box1.center, 16 * dt)
	self.box.center = I(self.center)

	if not self.ending and self.center == self.box1.center:
		if pygame.K_BACKSPACE in controls.kdowns:
			self.text = self.text[:-1]
		if pygame.K_TAB in controls.kdowns:
			self.text = ""
			sound.play("no")
		for char in acceptedchars:
			if char in controls.kdowns:
				self.text += char
		self.text = self.text[:32]

		if pygame.K_RETURN in controls.kdowns:
			self.ending = True
			sound.play("place")

def draw():
	background.draw()
	pview.fill((200, 200, 255, 64), T(self.box))
	if self.text:
		c = "|" if pygame.time.get_ticks() / 300 % 1 > 0.5 else u"\u00A0"
		ptext.draw(self.text + c, center = T(self.box.center), width = T(self.box.width),
			fontsize = T(34), fontname = "ChelaOne",
			color = "#ffffaa", shade = 1, shadow = (1, 1))
	else:
		ptext.draw("enter name", center = T(self.box.center), width = T(self.box.width),
			fontsize = T(26), fontname = "ChelaOne",
			color = "#ffffaa", shade = 1, shadow = (1, 1), alpha = 0.5)

	if self.center == self.box1.center:
		ptext.draw("Numbers and letters only. Enter to accept. Tab to clear.",
			midtop = T(640, 420), width = T(420),
			color = "#aabbff", shade = 1,
			fontsize = T(32), fontname = "ChelaOne", shadow = (1, 1)
		)



