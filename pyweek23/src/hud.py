import pygame
from . import ptext, state, view, state, util, image
from .util import F

def draw():
#	box = pygame.Surface(F(50, 50)).convert_alpha()
#	box.fill((80, 80, 80))
#	box.fill((20, 20, 20), F(1, 1, 48, 48))
#	ptext.draw("hp: %d/%d" % (state.hp, state.hp0), F(4, 4), surf = box, shadow = (1, 1), fontsize = F(14))
#	view.screen.blit(box, F(3, 3))
	for jhp in range(state.hp0):
		imgname = "health" if jhp < state.hp else "health0"
		pos = 20 + 16 * jhp, 30
		image.Fdraw(imgname, pos, scale = 0.3)
	for jhp in range(state.shieldhp0):
		a = util.clamp(state.shieldhp - jhp, 0, 1)
		imgname = "shield" if a == 1 or a * 20 % 2 > 1 else "health0"
		pos = 20 + 16 * (jhp + state.hp0), 30
		image.Fdraw(imgname, pos, scale = 0.3)
		


