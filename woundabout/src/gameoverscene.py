import pygame, math
from . import playscene, view, pview, ptext, scene, sound
from .pview import T


class self:
	pass

def init():
	self.t = 0

def think(dt, kpressed, kdowns):
	self.t += dt
	if self.t > 0.5 and "act" in kdowns:
		sound.playsound("blip1")
		if scene.current == "gameover_endless":
			scene.current = "endless"
			playscene.init()
		if scene.current == "gameover_adventure":
			scene.current = "adventure"
			playscene.init()

def draw():
	alpha = int(math.fadebetween(self.t, 0, 0, 1, 0.75) * 255)
	pview.fill((0, 0, 10, alpha))
	alpha = math.fadebetween(self.t, 0.2, 0, 1, 1)
	if alpha > 0:
		ptext.draw("Game over", center = T(640, 300), fontsize = T(200), 
			owidth = 0.5, alpha = alpha)
		ptext.draw("Space: continue", center = T(640, 480), fontsize = T(120), 
			owidth = 0.5, alpha = alpha)
