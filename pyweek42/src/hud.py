from . import ptext, pview
from .pview import T


def init():
	pass

def think(dt):
	pass

def draw():
	text = "Arrows or WASD: avoid the hazards"
	ptext.draw(text, midbottom = T(640, 700), width = T(900), fontsize = T(40), bold = True,
		color = (255, 200, 255), gcolor = (100, 255, 100), owidth = 1)


