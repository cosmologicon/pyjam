from __future__ import division
import pygame, math, random, time
from pygame.locals import *
from src import window, thing, settings, state, hud, quest, background, dialog, sound, image
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
	sound.playintromusic()

def think(dt, events, kpressed):
	kx = kpressed["right"] - kpressed["left"]
	ky = kpressed["up"] - kpressed["down"]

	dt0 = dt
	if kpressed["go"] and control:
		dt *= 0.3

	hud.think(dt0)
	quest.think(dt)
	dialog.think(dt0)
	background.flowt += dt

	for event in events:
		if event.type == KEYDOWN and event.key == "go":
			control.clear()
			control["cursor"] = state.you
			control["queue"] = {}
			control["qtarget"] = [state.you.X, state.you.y]
		if event.type == KEYUP:
			if not state.quickteleport and "queue" in control and event.key in ("up", "left", "right", "down"):
				control["queue"][event.key] = 0
		if event.type == KEYUP and event.key == "go" and "cursor" in control:
			if control["cursor"] is not state.you:
				state.effects.append(
					thing.Teleport(X = state.you.X, y = state.you.y, targetid = control["cursor"].thingid)
				)
				sound.play("teleport")
				state.you = control["cursor"]
			control.clear()

	if kpressed["go"] and control:
		if state.quickteleport:
			control["qtarget"][0] += kx * dt0 * settings.vqteleport / control["qtarget"][1]
			control["qtarget"][1] += ky * dt0 * settings.vqteleport
			dx = math.Xmod(control["qtarget"][0] - state.you.X) * state.you.y
			dy = control["qtarget"][1] - state.you.y
			f = math.sqrt(dx ** 2 + dy ** 2) / settings.rqteleport
			if f > 1:
				dx /= f
				dy /= f
				control["qtarget"] = [state.you.X + dx / state.you.y, state.you.y + dy]
			retarget()
		else:
			q = control["queue"]
			for key in q:
				q[key] += dt0
				if q[key] >= settings.jumpcombotime:
					dx = ("right" in q) - ("left" in q)
					dy = ("up" in q) - ("down" in q)
					jump(dx, dy)
					q.clear()
					break
	else:
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

def retarget():
	target = None
	d2 = 4 * settings.rqteleport ** 2
	X, y = control["qtarget"]
	for ship in state.ships:
		if window.distance(ship, state.you) > settings.rqteleport:
			continue
		dx = math.Xmod(ship.X - X) * (ship.y + y) / 2
		dy = ship.y - y
		if dx ** 2 + dy ** 2 < d2:
			target = ship
			d2 = dx ** 2 + dy ** 2
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
		image.worlddraw("cursor", control["cursor"].X, control["cursor"].y, 1.6,
			angle = pygame.time.get_ticks() * 0.15)
	if "qtarget" in control:
		X, y = control["qtarget"]
		image.worlddraw("qtarget", X, y, 1,
			angle = -pygame.time.get_ticks() * 0.15)
	dialog.draw()
	hud.draw()


