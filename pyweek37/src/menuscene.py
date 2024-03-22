import pygame, math
from . import pview, ptext, control, colorscene, settings, graphics, scene, state
from .pview import T

class self:
	pass

def init():
	self.t = 0
	control.init()
	texts = ["Tutorial", "Easy Mode", "Hard Mode"]
	rectVs = [pygame.Rect(0, 0, 500, 100) for text in texts]
	for j, rectV in enumerate(rectVs):
		rectV.center = 1000, 200 + 130 * j
	self.boxes = [(rectV, text) for rectV, text in zip(rectVs, texts)]
	self.selected = None
	self.done = False
	self.tdone = 0

def think(dt):
	self.t += dt
	if not self.done:
		self.selected = None
		for rectV, text in self.boxes:
			if T(rectV).collidepoint(control.posD):
				self.selected = text
		if self.selected is not None and control.click:
			self.done = True
	else:
		self.tdone += dt
		if self.tdone > 0.2:
			from . import playscene
			if settings.palette is None:
				scene.scene = colorscene
			else:
				scene.scene = playscene
			state.level = self.selected
			scene.scene.init()

def drawbox(rectV, text):
	sizeD = T(rectV.h * 0.8)
	pygame.draw.rect(pview.screen, (255, 255, 255), T(rectV), width = T(3),
		border_radius = T(10))
	ptext.draw(text, center = T(rectV).center, fontsize = sizeD,
		owidth = 1)

def draw():
	pview.fill((60, 40, 20))
	
	for rectV, text in self.boxes:
		drawbox(rectV, text)
	ptext.draw(settings.gamename, center = T(400, 400), width = T(600), fontsize = T(100),
		shade = 1, owidth = 1)
	ptext.draw("by Christopher Night\nmusic by Kevin MacLeod",
		bottomleft = T(20, 700), fontsize = T(40),
		shade = 1, owidth = 1)

	if self.t < 0.2:
		alpha = int(math.interp(self.tdone, 0, 255, 0.2, 0))
		pview.fill((0, 0, 0, alpha))
	if self.tdone:
		alpha = int(math.interp(self.tdone, 0, 0, 0.2, 255))
		pview.fill((0, 0, 0, alpha))

