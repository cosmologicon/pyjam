import pygame
from . import ptext, state, util, image, settings
from .pview import T

def draw():
	for jhp in range(state.hp0):
		imgname = "health" if jhp < state.hp else "health0"
		pos = 20 + 16 * jhp, 30
		image.Fdraw(imgname, pos, scale = 0.3)
	for jhp in range(state.shieldhp0):
		a = util.clamp(state.shieldhp - jhp, 0, 1)
		imgname = "shield" if a == 1 or a * 20 % 2 > 1 else "health0"
		pos = 20 + 16 * (jhp + state.hp0), 30
		image.Fdraw(imgname, pos, scale = 0.3)
	if settings.miracle:
		ptext.draw("Miracle Mode", topright = T(475 if settings.portrait else 850, 4),
			fontsize = T(20), fontname = "Bungee", owidth = 1)

