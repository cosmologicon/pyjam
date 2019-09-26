# Draw the right-hand panel
# TODO: let you click on the panel to go between stations

import pygame, math
from . import pview, state, view, ptext
from .pview import T


def stationat(mpos):
	for station in state.stations:
		yV = pview.I(math.fadebetween(station.z, 0, T(660), state.top, T(60)))
		rect = T(pygame.Rect(0, 0, 150, 20))
		rect.center = T(1140), yV
		if rect.collidepoint(mpos):
			return station
	return None


def draw(pstation):
	# TODO: bezeled edge for this rectangle, or some kind of fancy border.
	rect = T(1000, 0, 280, 720)
	pview.screen.fill((100, 80, 80), rect)
	# TODO: this is named wrong. View coordinates are before the T transformation is applied.
	yVbottom = T(660)
	yVtop = T(60)

	rect = T(pygame.Rect(0, 0, 20, 20))
	rect.centerx = T(1140)
	rect.centery = pview.I(math.fadebetween(view.zW0, 0, yVbottom, state.top, yVtop))
	pview.screen.fill((140, 100, 100), rect)

	for A in range(8):
		xV = T(1140 - 15 * view.dA(A, view.A))
		color = (220, 220, 220) if abs(view.dA(A, view.A)) < 0.1 else (110, 110, 110)
		pygame.draw.line(pview.screen, color, (xV, yVtop), (xV, yVbottom), T(3))

	for station in state.stations:
		yV = pview.I(math.fadebetween(station.z, 0, yVbottom, state.top, yVtop))
		rect = T(pygame.Rect(0, 0, 140, 6))
		rect.center = T(1140), yV
		color = (255, 255, 255) if station is pstation else (140, 255, 255)
		pview.screen.fill(color, rect)
		ptext.draw(station.name, bottomleft = rect.topleft, color = color, ocolor = (0, 40, 40),
			fontsize = T(16), owidth = 1)
		if station.quests:
			ptext.draw("(!)", center = (T(1050), yV), color = "yellow",
				fontsize = T(28), owidth = 1.5)

	for car in state.cars:
		xV = T(1140 - 15 * view.dA(car.A, view.A))
		yV = pview.I(math.fadebetween(car.z, 0, yVbottom, state.top, yVtop))
		fcolor = (0, 0, 0) if not car.held else (255, 255, 255)
		pygame.draw.circle(pview.screen, (255, 100, 100), (xV, yV), T(6))
		pygame.draw.circle(pview.screen, fcolor, (xV, yV), T(4))

	return


	pygame.draw.line(pview.screen, (220, 220, 220), (xV, yVtop), (xV, yVbottom), T(3))
	for car in state.cars:
		yV = pview.I(math.fadebetween(car.z, 0, yVbottom, state.top, yVtop))
		rect = T(pygame.Rect(0, 0, 4, 4))
		rect.center = xV, yV
		pview.screen.fill((255, 100, 100), rect)
		
	

