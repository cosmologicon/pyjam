from __future__ import division
import pygame, math, random, time
from pygame.locals import *
from src import window, thing, settings, state, hud, quest, background, dialog
from src.window import F


y0 = 1000

control = {}

def init():
	quest.quests["Intro"].available = True
	state.you = thing.Trainer(X = 0, y = y0, vx = 0, vy = 0)
	state.ships = [state.you]
	for j in range(6):
		a = j * math.tau / 6
		state.ships.append(thing.Trainer(X = 8 * math.cos(a) / y0, y = y0 + 8 * math.sin(a), vx = 0, vy = 0))
	state.objs = []
	state.filaments = []
	state.hazards = []

def think(dt, events, kpressed):
	kx = kpressed[K_RIGHT] - kpressed[K_LEFT]
	ky = kpressed[K_UP] - kpressed[K_DOWN]

	dt0 = dt
	if kpressed[K_SPACE]:
		dt *= 0.3

	hud.think(dt0)
	quest.think(dt)
	dialog.think(dt0)

	for event in events:
		if event.type == KEYDOWN and event.key == K_SPACE:
			control.clear()
			control["cursor"] = state.you
			control["queue"] = {}
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
	state.you.vy += dvy

	state.you.think(0)  # Clear out any controls that should be overridden
	for ship in state.ships:
		ship.think(dt)
		dx = y0 * ship.X
		dy = ship.y - y0
		f = math.sqrt(dx ** 2 + dy ** 2) / 15
		if f > 1:
			ship.X /= f
			ship.y = y0 + dy / f
			ship.vx = 0
			ship.vy = 0
	for effect in state.effects:
		effect.think(dt)
	state.effects = [e for e in state.effects if e.alive]

	window.camera.X0 = 0
	window.camera.y0 = y0
	window.camera.R = window.sy / 32

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
	window.screen.fill((0, 0, 0))
	background.drawstars()
	for ship in state.ships:
		ship.draw()
	for effect in state.effects:
		effect.draw()
	if "cursor" in control:
		pos = control["cursor"].screenpos()
		pygame.draw.circle(window.screen, (200, 100, 0), pos, window.F(15), 1)
	dialog.draw()
	hud.draw()


