import pygame, math
from . import pview, ptext, control, colorscene, settings, graphics, scene, state, render, view, sound
from .pview import T

class self:
	pass

def init():
	self.t = 0
	control.init()
	texts = ["tutorial", "easy", "hard"]
	rectVs = [pygame.Rect(0, 0, 400, 100) for text in texts]
	for j, rectV in enumerate(rectVs):
		rectV.center = 1000, 200 + 130 * j
	self.boxes = [(rectV, text) for rectV, text in zip(rectVs, texts)]
	self.selected = None
	self.done = False
	self.tdone = 0
	sound.playmusic("notasitseems")

def think(dt):
	self.t += dt
	if not self.done:
		self.selected = None
		for rectV, name in self.boxes:
			if T(rectV).collidepoint(control.posD):
				self.selected = name
		if self.selected is not None and control.click:
			self.done = True
	else:
		self.tdone += dt
		if self.tdone > 0.2:
			from . import playscene
			pview.centerx0, pview.centery0 = pview.center0
			if settings.palette is None:
				scene.scene = colorscene
			else:
				scene.scene = playscene
			state.level = self.selected
			view.tilt = 0.15
			view.tip = 0.7
			scene.scene.init()
			sound.play("advance")

def drawbox(rectV, name):
	text = {
		"tutorial": "Tutorial",
		"easy": "Easy Mode",
		"hard": "Hard Mode",
	}[name]
	sizeD = T(rectV.h * 0.7)
	pygame.draw.rect(pview.screen, (60, 60, 120), T(rectV),
		border_radius = T(10))
	pygame.draw.rect(pview.screen, (128, 128, 255), T(rectV), width = T(5),
		border_radius = T(10))
	ptext.draw(text, center = T(rectV).center, fontsize = sizeD,
		color = (128, 128, 255), shade = 0.4,
		fontname = "BebasNeue", shadow = (0.3, 0.3), owidth = 0.1)

def draw():
	pview.fill((60, 40, 20))

	view.tilt = 0.04 * 0.001 * pygame.time.get_ticks()
	render.setcamera()
	img = render.renderdome(T(300))
#	img = pygame.transform.smoothscale(img, T(600, 600))
	pview.screen.blit(img, img.get_rect(center = T(400, 420)))
	
	for rectV, name in self.boxes:
		drawbox(rectV, name)
	ptext.draw(settings.gamename, midtop = T(400, 40), width = T(600),
		color = (200, 200, 255),
		fontname = "RussoOne", fontsize = T(80),
		shade = 1, owidth = 0.5, shadow = (1, 1))
	ptext.draw("by Christopher Night\nmusic by Kevin MacLeod",
		bottomleft = T(20, 700), fontname = "RussoOne", fontsize = T(40),
		shade = 1, owidth = 1)

	lines = [
		"F10: change resolution",
		"F11: toggle fullscreen",
		"See README.txt for more settings.",
	]
	ptext.draw("\n".join(lines), bottomright = T(1262, 710), fontsize = T(19),
		fontname = "RussoOne", owidth = 0.5, color = (200, 200, 255), shade = 0.5)


	if self.t < 0.2:
		alpha = int(math.interp(self.tdone, 0, 255, 0.2, 0))
		pview.fill((0, 0, 0, alpha))
	if self.tdone:
		alpha = int(math.interp(self.tdone, 0, 0, 0.2, 255))
		pview.fill((0, 0, 0, alpha))

