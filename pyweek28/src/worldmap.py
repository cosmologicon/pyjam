# Draw the right-hand panel
# TODO: let you click on the panel to go between stations

import pygame, math
from . import pview, state, view, ptext
from .pview import T

def draw():
	# TODO: bezeled edge for this rectangle, or some kind of fancy border.
	rect = T(1000, 0, 280, 720)
	pview.screen.fill((100, 80, 80), rect)
	yVbottom = T(660)
	yVtop = T(60)
	xV = T(1140)

	rect = T(pygame.Rect(0, 0, 20, 20))
	rect.centerx = xV
	rect.centery = pview.I(math.fadebetween(view.yG0, 0, yVbottom, state.top, yVtop))
	pview.screen.fill((140, 100, 100), rect)

	pygame.draw.line(pview.screen, (220, 220, 220), (xV, yVtop), (xV, yVbottom), T(3))
	for station in state.stations:
		yV = pview.I(math.fadebetween(station.yG, 0, yVbottom, state.top, yVtop))
		rect = T(pygame.Rect(0, 0, 10, 6))
		rect.center = xV, yV
		pview.screen.fill((180, 255, 255), rect)
		if station.quests:
			ptext.draw("(!)", center = (xV + T(30), yV), color = "yellow",
				fontsize = T(28), owidth = 1.5)
	pygame.draw.line(pview.screen, (220, 220, 220), (xV, yVtop), (xV, yVbottom), T(3))
	

