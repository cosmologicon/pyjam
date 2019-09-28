# Draw the right-hand panel

import pygame, math
from functools import lru_cache
from . import pview, state, view, ptext
from .pview import T

# In view coordinates
def pos(z, A):
	px = T(1190 - 15 * view.dA(A, view.A))
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

@lru_cache(1)
def backdrop(w, h):
	surf = pygame.Surface((w, h)).convert_alpha()
	surf.fill((100, 100, 255, 70))
	rect = pygame.Rect((0, 0, w, h))
	rect.inflate_ip(-w // 12, -w // 12)
	surf.fill((100, 100, 255, 50), rect)
	return surf


def draw(pstation, pcar):
	pview.screen.blit(backdrop(T(180), T(720)), T(1100, 0))
	# TODO: this is named wrong. View coordinates are before the T transformation is applied.
	yVbottom = T(660)
	yVtop = T(60)

	rect = T(pygame.Rect(0, 0, 20, 20))
	rect.center = pos(view.zW0, view.A)
	pview.screen.fill((100, 100, 255), rect)

	for A in range(8):
		color = (220, 220, 220) if abs(view.dA(A, view.A)) < 0.1 else (110, 110, 110)
		pygame.draw.line(pview.screen, color, pos(0, A), pos(state.top, A), T(3))

	for station in state.stations:
		rect = T(pygame.Rect(0, 0, 140, 6))
		rect.center = pos(station.z, view.A)
		color = (255, 255, 255) if station is pstation else (140, 255, 255)
		if station.mission and station.mission.fulfilled():
			ptext.draw("(!)", center = (T(1105), rect.centery), color = "yellow",
				fontsize = T(28), owidth = 1.5, fontname = "RobotoCondensed-Bold")
			if pygame.time.get_ticks() * 0.001 % 1 > 0.5:
				color = 255, 200, 20
		pview.screen.fill(color, rect)
		ptext.draw(station.name, bottomleft = rect.topleft, color = color, ocolor = (0, 40, 40),
			fontsize = T(19), owidth = 1, fontname = "RobotoCondensed-Bold")
		rect = pygame.Rect(rect.left + T(4), rect.bottom + T(2), T(8), T(8))
		for j in range(station.showncapacity()):
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
			if station in car.stationtargets():
				ptext.draw("O", center = pos(station.z, car.A), color = "blue", ocolor = "white", fontsize = T(14), owidth = 1)
				
			

	for car in state.cars:
		p = pos(car.z, car.A)
		fcolor = (0, 0, 0) if not car.held else (255, 255, 255)
		if car is pcar:
			pygame.draw.circle(pview.screen, (255, 255, 255), p, T(8))
		pygame.draw.circle(pview.screen, (255, 100, 100), p, T(6))
		pygame.draw.circle(pview.screen, fcolor, p, T(4))
		if car.broken:
			r = math.mix(8, 16, math.sqrt(0.005 * pygame.time.get_ticks() % 1))
			pygame.draw.circle(pview.screen, (255, 100, 100), p, T(r), T(2))
	

