import pygame, math
from . import pview, ptext, control, colorscene, settings, graphics, scene, sound
from .pview import T

class self:
	pass

def init():
	self.t = 0
	control.init()
	palettes = list(settings.PALETTES.keys())
	rectVs = [pygame.Rect(0, 0, 430, 100) for palette in palettes]
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
		if self.tdone > 0.2:
			from . import playscene
			scene.scene = playscene
			sound.play("advance")
			playscene.init()
			settings.palette = self.selected
			settings.save()

def drawbox(rectV, palette, jpalette):
	sizeD = T(rectV.h * 0.8)
	dxD = 1.0 * sizeD
	t = 0.001 * pygame.time.get_ticks()
	for j, symbol in enumerate(settings.colors):
		t0 = math.fuzzrange(0, 100, 3900, jpalette, j)
		omega = math.fuzzrange(0.3, 0.4, 3901, jpalette, j)
		strength = math.mix(0.8, 1, math.cycle(t0 + omega * t))
		xD, yD = T(rectV.center)
		xD += int((j - (len(settings.colors) - 1) / 2) * dxD)
		t0 = math.fuzzrange(0, 100, 3900, jpalette, j)
		omega = math.fuzzrange(1, 1.5, 3901, jpalette, j)
		yD += T(5 * math.sin(t0 + omega * t))
		graphics.drawsymbolatD(symbol, (xD, yD), sizeD, strength = strength, palette = palette)
	graphics.renderqueue()
	if self.selected == palette:
		pygame.draw.rect(pview.screen, (200, 200, 255), T(rectV), width = T(5),
			border_radius = T(10))

text = "Please select your preferred color palette. Distinguishing the colors is not required for gameplay but it helps. See README.txt for more."

def draw():
	pview.fill((120, 100, 80))
	
	for j, (rectV, palette) in enumerate(self.boxes):
		drawbox(rectV, palette, j)
	ptext.draw(text, midbottom = T(640, 690), width = T(800), fontsize = T(40),
		color = (255, 255, 200),
		fontname = "OdibeeSans", shade = 0.6, owidth = 0.3, shadow = (1, 1))

	if self.t < 0.5:
		alpha = int(math.interp(self.tdone, 0, 255, 0.2, 0))
		pview.fill((0, 0, 0, alpha))
	if self.tdone:
		alpha = int(math.interp(self.tdone, 0, 0, 0.2, 255))
		pview.fill((0, 0, 0, alpha))

	
