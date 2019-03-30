import pygame, math
from . import pview, ptext, background, settings, hud, view
from . import scene, textscene, uploadscene, frostscene
from .pview import T

class self:
	pass

Fspot1 = (640, 360), 320

def init(design, Fspot, stage):
	self.design = design
	self.Fspot0 = Fspot
	self.Fspot = Fspot
	self.stage = stage
	self.a = 0
	
	self.buttons = [
		hud.Button(((640 - 360, 620), 80), "Share to\npublic\ngallery"),
		hud.Button(((640 + 360, 620), 80), "Next\nstage"),
		hud.Button(((1180, 620), 80), "Quit\nto menu"),
	]
	self.done = False

def think(dt, controls):
	background.update(dt)
	self.Fspot = view.Fspotapproach(self.Fspot, Fspot1, 10 * dt)
	if self.Fspot == Fspot1:
		self.a = math.approach(self.a, 1, 4 * dt)
	self.jbutton = None

	if self.a == 1:
		for jbutton, button in enumerate(self.buttons):
			if button.contains(controls.mpos):
				self.jbutton = jbutton

	if self.a == 1 and controls.mdown and not self.done:
		if self.jbutton is not None:
			onclick(self.buttons[self.jbutton])

def onclick(button):
	if "Quit" in button.text:
		self.done = True
		scene.push(frostscene)
		
	if "Next" in button.text:
		from . import playscene
		self.done = True
		scene.push(playscene, "stage2", depth=1)
		scene.push(frostscene)
	
	if "Share" in button.text:
		scene.push(uploadscene, self.design, Fspot1)
	
def draw():
	background.draw()
	self.design.draw(self.Fspot)
	if self.a >= 1:
		for jbutton, button in enumerate(self.buttons):
			button.draw(lit = (jbutton == self.jbutton))
		


