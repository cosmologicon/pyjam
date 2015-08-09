import pygame, math, random
from pygame.locals import *
from src import window, thing


def init():
	global you, ships
	you = thing.Skiff(X = 0, y = 100, vx = 8)
	ships = [you]
	for _ in range(100):
		ships.append(thing.Skiff(
			X = random.uniform(0, math.tau),
			y = random.uniform(50, 150),
			vx = random.uniform(-20, 20)
		))

def think(dt, events, kpressed):
	kx = kpressed[K_RIGHT] - kpressed[K_LEFT]
	ky = kpressed[K_UP] - kpressed[K_DOWN]

	if kpressed[K_SPACE]:
		dt *= 0.3

	for event in events:
		if event.type == KEYUP and event.key == K_SPACE:
			if kx or ky:
				jump(kx, ky)

	dvx = kx * dt * 20
#	dvy = ky * dt * 20

	if dvx:
		you.vx += dvx

	for ship in ships:
		ship.think(dt)

	window.cameraX0 = you.X
	window.cameray0 = you.y
	
def jump(kx, ky):
	global you
	target = None
	d2 = 20 ** 2
	for ship in ships:
		if ship is you:
			continue
		dx = math.Xmod(ship.X - you.X) * you.y
		dy = ship.y - you.y
		if dx * dx + dy * dy < d2:
			if abs(math.Xmod(math.atan2(kx, ky) - math.atan2(dx, dy))) < math.tau / 16:
				target = ship
				d2 = dx * dx + dy * dy
	if target:
		you = target

			


def draw():
	for y in range(10, 200, 10):
		for jX in range(20):
			X = math.tau * jX / 20
			p = window.screenpos(X, y)
			pygame.draw.circle(window.screen, (0, 100, 0), p, window.F(3))
	for ship in ships:
		ship.draw()


