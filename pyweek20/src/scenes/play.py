import pygame, math
from pygame.locals import *
from src import window, thing


def init():
	global you
	you = thing.add(thing.Skiff(X = 0, y = 100))

def think(dt, events, kpressed):
	dX = (kpressed[K_RIGHT] - kpressed[K_LEFT]) * dt * 0.1
	dy = (kpressed[K_UP] - kpressed[K_DOWN]) * dt * 10
	window.cameraX0 += dX
	window.cameray0 += dy

def draw():
	for y in range(10, 200, 10):
		for jX in range(20):
			X = math.tau * jX / 20
			p = window.screenpos(X, y)
			pygame.draw.circle(window.screen, (0, 100, 0), p, window.F(3))
	thing.get(you).draw()


