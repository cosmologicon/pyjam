# Draw the right-hand panel

import pygame, math
from . import pview, state, view, ptext
from .pview import T

# In actual screen coordinates (not view coordinates)
def pos(z, A):
	px = T(1140 - 15 * view.dA(A, view.A))
	py = pview.I(math.fadebetween(z, 0, T(660), state.top, T(60)))
	return px, py


def stationat(mpos):
	for station in state.stations:
		rect = T(pygame.Rect(0, 0, 150, 20))
		rect.center = pos(station.z, view.A)
		if rect.collidepoint(mpos):
			return station
	return None

def carat(mpos):
	for car in state.cars:
		carpos = pos(car.z, car.A)
		if math.distance(carpos, mpos) < T(12):
			return car
	return None


def draw(pstation, pcar):
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
		color = (220, 220, 220) if abs(view.dA(A, view.A)) < 0.1 else (110, 110, 110)
		pygame.draw.line(pview.screen, color, T(pos(0, A)), T(pos(state.top, A)), T(3))

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
		rect = T(pygame.Rect(rect.left + 4, rect.bottom + 2, 8, 8))
		for j in range(station.capacity):
			if j < len(station.held):
				color = station.held[j].color()
			elif j < len(station.held) + len(station.pending):
				color = math.imix(station.pending[j - len(station.held)].color(), (0, 0, 0), 0.5)
			else:
				color = 10, 10, 10
			pview.screen.fill(color, rect)
			color = math.imix(color, (0, 0, 0), 0.5)
			pview.screen.fill(color, rect.inflate(T(-2), T(-2)))
			rect.move_ip(T(9), 0)
		for A, blocked in enumerate(station.blocked):
			if blocked:
				ptext.draw("X", center = pos(station.z, A), color = "red", ocolor = "white", fontsize = T(14), owidth = 1)
			

	for car in state.cars:
		xV = T(1140 - 15 * view.dA(car.A, view.A))
		yV = pview.I(math.fadebetween(car.z, 0, yVbottom, state.top, yVtop))
		fcolor = (0, 0, 0) if not car.held else (255, 255, 255)
		if car is pcar:
			pygame.draw.circle(pview.screen, (255, 255, 255), (xV, yV), T(8))
		pygame.draw.circle(pview.screen, (255, 100, 100), (xV, yV), T(6))
		pygame.draw.circle(pview.screen, fcolor, (xV, yV), T(4))
		if car.broken:
			r = math.mix(8, 16, math.sqrt(0.005 * pygame.time.get_ticks() % 1))
			pygame.draw.circle(pview.screen, (255, 100, 100), (xV, yV), T(r), T(2))
	

