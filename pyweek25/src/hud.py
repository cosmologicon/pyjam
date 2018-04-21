import pygame, math
from . import pview, ptext, cstate, tile, state
from .pview import T

controls = []

def getpointed(mposV):
	for j, control in enumerate(controls):
		xV, yV = 50, 50 + 100 * j
		if math.distance(mposV, (xV, yV)) < 40:
			return control

def think(dt):
	pass

def draw(players):
	for j, control in enumerate(controls):
		xV, yV = 50, 50 + 100 * j
		color = (200, 200, 200) if control == cstate.cursor else (50, 50, 50)
		img = tile.getimg("button", T(80), color)
		pview.screen.blit(img, img.get_rect(center = T(xV, yV)))
		ptext.draw(control, center = T(xV, yV), fontsize = T(30), owidth = 1, ocolor = "black",
			color = "white", fontname = "Passion")
	img = tile.getimg("part", T(70))
	pview.screen.blit(img, img.get_rect(topright = pview.topright))
	score = sum(state.scores[who] for who in players)
	ptext.draw("%s/%s" % (score, state.goal), fontsize = T(50), fontname = "Passion",
		top = T(30), right = pview.right - 70,
		ocolor = "black", owidth = 2, shade = 2)


