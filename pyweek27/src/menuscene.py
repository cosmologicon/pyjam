from __future__ import division
import random, math, pygame
from . import pview, thing, flake, background, ptext, render, shape, view, hud, frostscene, scene, playscene
from .pview import T

class self:
	pass

def init():
	self.buttons = [
		hud.Button((pview.center0, pview.s0 / 6), "play"),
	]

def think(dt, controls):
	background.update(dt)

	self.jbutton = None
	for jbutton, button in enumerate(self.buttons):
		if button.contains(controls.mpos):
			self.jbutton = jbutton

	if self.jbutton is not None and controls.mdown:
		onclick(self.buttons[self.jbutton])

def onclick(button):
	if button.text == "play":
		scene.push(playscene)
		scene.push(frostscene, up=True)

def draw():
	pygame.mouse.set_visible(True)
	background.draw()

	for jbutton, button in enumerate(self.buttons):
		button.draw(lit = (jbutton == self.jbutton))

