from __future__ import division
import pygame, math, random, time
from pygame.locals import *
from src import window, thing, settings, state, hud, quest, background, dialog


control = {}

def init():
	quest.quests["FirstSatellite"].available = True
	state.you = thing.Beacon(X = 0, y = state.R - 10, vx = 1)
	state.ships = [state.you]
	state.objs = []
	state.filaments = [thing.Filament(ladderps = state.worlddata["filaments"][0])]
	state.hazards = [
		thing.Tremor(X = random.uniform(0, math.tau), y = random.uniform(0, state.R))
		for _ in range(100)
	]


def think(dt, events, kpressed):
	kx = kpressed[K_RIGHT] - kpressed[K_LEFT]
	ky = kpressed[K_UP] - kpressed[K_DOWN]

	dt0 = dt
	if kpressed[K_SPACE]:
		dt *= 0.3

	hud.think(dt0)
	quest.think(dt)
	dialog.think(dt0)

	if random.random() < dt:
		state.ships.append(thing.Skiff(
			X = random.uniform(0, math.tau),
			y = state.R,
			vx = random.uniform(-6, 6)
		))
		state.ships.append(thing.CommShip(
			X = random.uniform(0, math.tau),
			y = state.R,
			vx = random.uniform(-6, 6)
		))

	for event in events:
		if event.type == KEYDOWN and event.key == K_SPACE:
			control.clear()
			control["cursor"] = state.you
			control["queue"] = {}
		if event.type == KEYDOWN and event.key == K_LSHIFT:
			state.you.deploy()
		if event.type == KEYDOWN and event.key == K_BACKSPACE:
			state.ships.remove(state.you)
			thing.kill(state.you)
			state.you = thing.Skiff(X = 0, y = state.R - 10, vx = 1)
			state.ships.append(state.you)
		if event.type == KEYUP:
			if "queue" in control and event.key in (K_UP, K_LEFT, K_RIGHT, K_DOWN):
				control["queue"][event.key] = 0
		if event.type == KEYUP and event.key == K_SPACE:
			if control["cursor"] is not state.you:
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
	dvy = ky * dt * 20

	state.you.vx += dvx
	state.you.vy = min(state.you.vy + dvy, 0)

	state.you.think(0)  # Clear out any controls that should be overridden
	nships = []
	for ship in state.ships:
		ship.think(dt)
		if ship.alive:
			nships.append(ship)
		else:
			thing.kill(ship)
			if ship is state.you:
				print("TODO: handle dying")
	state.ships = nships
	nobjs = []
	for obj in state.objs:
		obj.think(dt)
		if obj.alive:
			nobjs.append(obj)
		else:
			thing.kill(obj)
	state.obj = nobjs
	for hazard in state.hazards:
		hazard.think(dt)
	state.obj = nobjs
#	for filament in state.filaments:
#		filament.think(dt)

	window.cameraX0 = state.you.X
	window.cameray0 = state.you.y
	window.cameraR = window.sy / 48

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
#	for y in range(10, 200, 10):
#		for jX in range(20):
#			X = math.tau * jX / 20
#			p = window.screenpos(X, y)
#			pygame.draw.circle(window.screen, (0, 100, 0), p, window.F(3))
	if settings.drawbackground:
		background.draw()
	else:
		window.screen.fill((0, 60, 0))
	for obj in state.objs:
		if window.onscreen(obj):
			obj.draw()
	for ship in state.ships:
		if window.onscreen(ship):
			ship.draw()
	for hazard in state.hazards:
		if window.onscreen(hazard):
			hazard.draw()
#	background.drawfilament()
	if "cursor" in control:
		pos = control["cursor"].screenpos()
		pygame.draw.circle(window.screen, (200, 100, 0), pos, window.F(15), 1)
	dialog.draw()
	hud.draw()
	state.you.drawhud()


