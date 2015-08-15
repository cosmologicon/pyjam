from __future__ import division
import pygame, math, random, time
from pygame.locals import *
from src import window, thing, settings, state, hud, quest, background, dialog, sound
from src.window import F


def init():
	global playing, tplay
	state.effects.append(thing.FirstConvergence(X = state.you.X, y = state.you.y))
	sound.epicness = 2
	sound.play("reveal")
	playing = False
	tplay = 0

def think(dt, events, kpressed):
	global todraw, tplay
	hud.think(dt)
	quest.think(dt)
	dialog.think(dt)
	background.think(dt)
	sound.think(dt)

	if playing:
		tplay += dt
		background.flowt += dt * 4
		if tplay > 3:
			dialog.play("convo9")
		if tplay > 6:
			background.wash()
			from src import scene
			from src.scenes import play
			scene.current = play
			state.you.tflash = settings.tcutsceneinvulnerability
		return

	nbubble = int(dt * 30) + (random.random() < dt * 30 % 1)
	for _ in range(nbubble):
		X = random.gauss(state.you.X, 30 / state.you.y)
		y = random.gauss(state.you.y, 30)
		if y < state.R - 10:
			state.effects.append(thing.Bubble(X = X, y = y))

	todraw = []
	scollide = []
	hcollide = []

	nships = []
	for ship in state.ships:
		if not window.camera.near(ship):
			nships.append(ship)
			continue
		ship.think(dt)
		if ship.alive:
			nships.append(ship)
			if window.camera.on(ship):
				todraw.append(ship)
		else:
			ship.die()
			if ship is state.you:
				regenerate()
	state.ships = nships
	nobjs = []
	for obj in state.objs:
		if not window.camera.on(obj):
			nobjs.append(obj)
			continue
		obj.think(dt)
		if obj.alive:
			nobjs.append(obj)
			todraw.append(obj)
		else:
			obj.die()
	state.obj = nobjs
	for hazard in state.hazards:
		if not window.camera.near(hazard):
			continue
		hazard.think(dt)
		todraw.append(hazard)
		if window.camera.on(hazard):
			hcollide.append(hazard)
	state.obj = nobjs
	neffects = []
	for effect in state.effects:
		effect.think(dt)
		if effect.alive:
			todraw.append(effect)
			neffects.append(effect)
		else:
			effect.die()
	state.effects = neffects
	window.camera.follow(state.you)
	window.camera.think(dt)

def draw():
	if playing:
		drawscene()
		return

	if settings.drawbackground:
		background.draw()
	else:
		window.screen.fill((0, 60, 0))
	for obj in todraw:
		obj.draw()

	dialog.draw()
	hud.draw()
	hud.drawstats()
	state.you.drawhud()
	background.drawwash()

def drawscene():
	window.screen.fill((20, 0, 0))
	R, X0, y0 = window.camera.R, window.camera.X0, window.camera.y0
	window.camera.R = window.sy / 54 * math.clamp(3 * (tplay - 4), 0.3, 2)
	window.camera.y0 = random.uniform(-1, 1)
	window.camera.X0 = tplay * 0.1
	background.draw(factor = 8)
	window.camera.R, window.camera.X0, window.camera.y0 = R, X0, y0
	background.drawwash()
	
	



