from __future__ import division
import random, math, pygame
from . import pview, thing, flake, background, ptext, render, shape, view, hud
from . import frostscene, scene, playscene, galleryscene, storyscene
from .pview import T

class self:
	pass

def init(page = "main"):
	self.page = page
	
	self.buttons = [
	]

	if self.page == "main":
		x, y = pview.center0
		s = pview.s0 / 12
		self.buttons += [
			hud.Button(((x - 4.5 * s, y), s), "Story"),
			hud.Button(((x - 1.5 * s, y), s), "Gallery"),
			hud.Button(((x + 1.5 * s, y), s), "Free\nPlay"),
			hud.Button(((x + 4.5 * s, y), s), "Bonus\nStages"),
		]
	if self.page == "story":
		x, y = pview.center0
		s = pview.s0 / 18
		self.buttons += [
			hud.Button(((x - 4.5 * s, y), s), "Stage 1"),
		]

def think(dt, controls):
	background.update(dt, (200, 200, 200))

	self.jbutton = None
	for jbutton, button in enumerate(self.buttons):
		if button.contains(controls.mpos):
			self.jbutton = jbutton

	if self.jbutton is not None and controls.mdown:
		onclick(self.buttons[self.jbutton])

def onclick(button):
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
		scene.push(frostscene, depth0 = 4)

def draw():
	pygame.mouse.set_visible(True)
	background.draw()
	ptext.draw(self.page, midtop = T(640, 20), owidth = 0.6,
		color = "#ffffff", shade = 1, fontsize = T(80), fontname = "GermaniaOne", shadow = (1, 1)
	)

	for jbutton, button in enumerate(self.buttons):
		button.draw(lit = (jbutton == self.jbutton))
