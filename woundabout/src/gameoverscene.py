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
			scene.setcurrent("endless")
		if scene.current == "gameover_adventure":
			scene.setcurrent("adventure")
	if self.t > 0.5 and "quit" in kdowns:
		sound.playsound("blip1")
		scene.setcurrent("menu")

def draw():
	alpha = int(math.fadebetween(self.t, 0, 0, 1, 0.75) * 255)
	pview.fill((0, 0, 10, alpha))
	alpha = math.fadebetween(self.t, 0.2, 0, 1, 1)
	if alpha > 0:
		ptext.draw("Game Over", center = T(640, 300), fontsize = T(120),
			owidth = 0.5, shadow = (1, 1), shade = 1, alpha = alpha)
		ptext.draw("Space/Enter: continue", center = T(640, 540), fontsize = T(60),
			owidth = 0.5, shadow = (1, 1), shade = 1, alpha = alpha)

