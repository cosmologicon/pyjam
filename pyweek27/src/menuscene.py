from __future__ import division
import random, math, pygame
from . import pview, thing, flake, background, ptext, render, shape, view, hud, progress, settings
from . import frostscene, scene, playscene, galleryscene, storyscene
from .pview import T

class self:
	pass

def init(page = "main"):
	self.page = page

	self.title = {
		"main": settings.gamename,
		"story": "Story/Tutorial",
		"bonus": "Bonus Stages",
	}[self.page]
	self.subtitle = {
		"main": "Universe Factory Games",
		"story": "",
		"bonus": "Complete to unlock abilities in Free Play mode",
	}[self.page]
	setbuttons()


def setbuttons():
	self.buttons = []

	if self.page == "main":
		self.buttons.append(hud.Button(((1200, 640), 50), "Quit"))
	else:
		self.buttons.append(hud.Button(((1200, 640), 50), "Main\nMenu"))

	if self.page == "main":
		x, y = pview.center0
		s = pview.s0 / 12
		self.buttons += [
			hud.Button(((x - 4.5 * s, y), s), "Story"),
		]
		if progress.donestory:
			self.buttons += [
				hud.Button(((x - 1.5 * s, y), s), "Gallery"),
				hud.Button(((x + 1.5 * s, y), s), "Free\nPlay"),
				hud.Button(((x + 4.5 * s, y), s), "Bonus\nStages"),
			]
	if self.page == "story":
		x, y = pview.center0
		s = pview.s0 / 14
		for j, (C, S) in enumerate(math.CSround(6, 2.4 * s), 1):
			if j > progress.stage:
				continue
			pos = 640 + S, 400 - C
			self.buttons += [
				hud.Button((pos, s), "Stage %s" % j),
			]

	if self.page == "bonus":
		x, y = pview.center0
		s = pview.s0 / 14
		for j in (1, 2, 3):
			dx = 1.2 * s * (j - 2)
			dy = 1.2 * math.sqrt(3) * s * (j - 2)
			if j <= progress.stageshapes:
				pos = 340 + dx, 400 + dy
				self.buttons += [hud.Button((pos, s), "Shape %s" % j)]
			if j <= progress.stagecolors:
				pos = 640 + dx, 400 + dy
				self.buttons += [hud.Button((pos, s), "Color %s" % j)]
			if j <= progress.stagesizes:
				pos = 940 + dx, 400 + dy
				self.buttons += [hud.Button((pos, s), "Size %s" % j)]


def think(dt, controls):
	if progress.check():
		setbuttons()
	background.update(dt, (200, 200, 200))

	self.jbutton = None
	for jbutton, button in enumerate(self.buttons):
		if button.contains(controls.mpos):
			self.jbutton = jbutton

	if self.jbutton is not None and controls.mdown:
		onclick(self.buttons[self.jbutton])

def onclick(button):
	if button.text == "Quit":
		scene.pop()
	if button.text == "Main\nMenu":
		scene.push(frostscene, onswap=lambda: init("main"))
	if button.text == "Story":
		scene.push(frostscene, onswap=lambda: init("story"))
	if button.text == "Free\nPlay":
		scene.push(playscene, "free")
		scene.push(frostscene, depth0 = 3)
	if button.text == "Bonus\nStages":
		scene.push(frostscene, onswap=lambda: init("bonus"))
	if button.text == "Gallery":
		scene.push(galleryscene)
		scene.push(frostscene, depth0 = 3)
	if button.text.startswith("Stage"):
		stage = button.text.replace(" ", "").lower()
		scene.push(playscene, stage)
		scene.push(storyscene, stage)
		scene.push(frostscene, depth0 = 4, onswap=lambda: init("main"))
	if button.text.startswith("Color") or button.text.startswith("Shape") or button.text.startswith("Size"):
		stage = button.text.replace(" ", "").lower()
		scene.push(playscene, stage)
		scene.push(frostscene, depth0 = 3)

def draw():
	pygame.mouse.set_visible(True)
	background.draw()
	ptext.draw(self.title, midtop = T(640, 20), owidth = 0.6,
		color = "#ffffff", shade = 1, fontsize = T(80), fontname = "GermaniaOne", shadow = (1, 1)
	)
	ptext.draw(self.subtitle, midtop = T(640, 120), owidth = 0.6,
		color = "#ffffdd", shade = 1, fontsize = T(40), fontname = "ChelaOne", shadow = (1, 1)
	)
	if self.page == "bonus" and progress.donebonus:
		ptext.draw("All stages complete. Thank you for playing.", midbottom = T(640, 700), owidth = 0.6,
			color = "#ffffdd", shade = 1, fontsize = T(40), fontname = "ChelaOne", shadow = (1, 1)
		)

	for jbutton, button in enumerate(self.buttons):
		button.draw(lit = (jbutton == self.jbutton))

