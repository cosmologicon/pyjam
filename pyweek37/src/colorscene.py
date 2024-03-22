import pygame
from . import pview, ptext, control, colorscene, settings, graphics, scene
from .pview import T

class self:
	pass

def init():
	self.t = 0
	control.init()
	palettes = list(settings.PALETTES.keys())
	rectVs = [pygame.Rect(0, 0, 500, 100) for palette in palettes]
	for j, rectV in enumerate(rectVs):
		rectV.center = 640, 200 + 130 * j
	self.boxes = [(rectV, palette) for rectV, palette in zip(rectVs, palettes)]
	self.selected = None
	self.done = False
	self.tdone = 0

def think(dt):
	self.t += dt
	if not self.done:
		self.selected = None
		for rectV, palette in self.boxes:
			if T(rectV).collidepoint(control.posD):
				self.selected = palette
		if self.selected is not None and control.click:
			self.done = True
	else:
		self.tdone += dt
		if self.tdone > 0.5:
			from . import playscene
			scene.scene = playscene
			playscene.init()
			settings.palette = self.selected
			settings.save()

def drawbox(rectV, palette):
	sizeD = T(rectV.h * 0.8)
	dxD = 1.0 * sizeD
	for j, symbol in enumerate(settings.colors):
		strength = 1
		xD, yD = T(rectV.center)
		xD += int((j - (len(settings.colors) - 1) / 2) * dxD)
		graphics.drawsymbolatD(symbol, (xD, yD), sizeD, strength = strength, palette = palette)
	graphics.renderqueue()
	if self.selected == palette:
		pygame.draw.rect(pview.screen, (255, 255, 255), T(rectV), width = T(3),
			border_radius = T(10))

text = "Please select your preferred color palette. Distinguishing the colors is not required for gameplay but it helps. See README.txt for more."

def draw():
	pview.fill((60, 40, 20))
	
	for rectV, palette in self.boxes:
		drawbox(rectV, palette)
	ptext.draw(text, midbottom = T(640, 690), width = T(800), fontsize = T(40),
		shade = 1, owidth = 1)

	
