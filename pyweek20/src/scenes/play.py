import pygame, math, random, time
from pygame.locals import *
from src import window, thing, settings, state, hud, quest


control = {}

def init():
	state.you = thing.Skiff(X = 0, y = 100, vx = 8)
	state.ships = [state.you]
	state.objs = []
	for _ in range(100):
		state.ships.append(thing.Skiff(
			X = random.uniform(0, math.tau),
			y = random.uniform(50, 150),
			vx = random.uniform(-20, 20)
		))
		state.ships.append(thing.CommShip(
			X = random.uniform(0, math.tau),
			y = random.uniform(50, 150),
			vx = random.uniform(-20, 20),
			vy = -0.3
		))
	for _ in range(100):
		state.objs.append(thing.Payload(
			X = random.uniform(0, math.tau),
			y = random.uniform(50, 150)
		))

def think(dt, events, kpressed):
	kx = kpressed[K_RIGHT] - kpressed[K_LEFT]
	ky = kpressed[K_UP] - kpressed[K_DOWN]

	dt0 = dt
	if kpressed[K_SPACE]:
		dt *= 0.3

	hud.think(dt0)
	quest.think(dt)

	for event in events:
		if event.type == KEYDOWN and event.key == K_SPACE:
			control.clear()
			control["cursor"] = state.you
			control["queue"] = {}
		if event.type == KEYDOWN and event.key == K_LSHIFT:
			state.you.deploy()
		if event.type == KEYUP:
			if "queue" in control and event.key in (K_UP, K_LEFT, K_RIGHT, K_DOWN):
				control["queue"][event.key] = 0
		if event.type == KEYUP and event.key == K_SPACE:
			if control["cursor"] != state.you:
				state.you = control["cursor"]
			control.clear()
		
	if kpressed[K_SPACE]:
		q = control["queue"]
		for key in q:
			q[key] += dt0
			if q[key] >= settings.jumpcombotime:
				dx = (K_RIGHT in q) - (K_LEFT in q)
				dy = (K_UP in q) - (K_DOWN in q)
				jump(dx, dy)
				q.clear()
				break

	dvx = kx * dt * 20
#	dvy = ky * dt * 20

	if dvx:
		state.you.vx += dvx

	state.you.think(0)  # Clear out any controls that should be overridden
	for ship in state.ships:
		ship.think(dt)
	for obj in state.objs:
		obj.think(dt)

	window.cameraX0 = state.you.X
	window.cameray0 = state.you.y

def jump(kx, ky):
	target = None
	d2 = settings.maxjump ** 2
	for ship in state.ships:
		if ship is control["cursor"]:
			continue
		dx = math.Xmod(ship.X - control["cursor"].X) * control["cursor"].y
		dy = ship.y - control["cursor"].y
		if dx * dx + dy * dy < d2:
			if abs(math.Xmod(math.atan2(kx, ky) - math.atan2(dx, dy))) < math.tau / 11:
				target = ship
				d2 = dx * dx + dy * dy
	if target:
		control["cursor"] = target


def draw():
	for y in range(10, 200, 10):
		for jX in range(20):
			X = math.tau * jX / 20
			p = window.screenpos(X, y)
			pygame.draw.circle(window.screen, (0, 100, 0), p, window.F(3))
	for obj in state.objs:
		obj.draw()
	for ship in state.ships:
		ship.draw()
	if "cursor" in control:
		pos = control["cursor"].screenpos()
		pygame.draw.circle(window.screen, (200, 100, 0), pos, window.F(15), 1)
	hud.draw()


