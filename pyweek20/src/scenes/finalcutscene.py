from __future__ import division
import pygame, math, random, time
from pygame.locals import *
from src import window, thing, settings, state, hud, quest, background, dialog, sound
from src.window import F

def init():
	global tplay

	window.camera.X0 = 0
	window.camera.y0 = 500
	window.camera.R = window.sy / 40
	sound.epicness = 2
	dialog.play("convo16")
	tplay = 0
	background.wash()
	state.you = getattr(thing, quest.quests["Finale"].winner)(X = 0, y = window.camera.y0 + 20)
	state.effects = []

def think(dt, events, kpressed):
	global todraw, tplay
	dialog.think(dt)
	background.think(dt)
	sound.think(dt)

	tplay += dt
	background.flowt += dt * 2

	state.you.y -= 1 * dt
	if tplay > 7 and state.you.alive:
		state.you.die()
		state.effects.append(
			thing.SlowTeleport(X = 0, y = state.you.y, X1 = 0, y1 = window.camera.y0 - 20)
		)
	if tplay > 10 and random.random() / (0.1 * tplay) < dt:
		state.effects.append(thing.SlowTeleport(
			X = random.gauss(0, 20 / window.camera.y0),
			y = random.gauss(window.camera.y0 - 14, 20),
			X1 = random.gauss(0, 20 / window.camera.y0),
			y1 = random.gauss(window.camera.y0 - 14, 20)
		))

	if tplay > 30:
		from src import scene
		from src.scenes import endtitle
		scene.current = endtitle
		scene.toinit = endtitle

	neffects = []
	for effect in state.effects:
		effect.think(dt/4)
		if effect.alive:
			neffects.append(effect)
		else:
			effect.die()
	state.effects = neffects

def draw():
	window.screen.fill((255, 255, 255))
	R, X0, y0 = window.camera.R, window.camera.X0, window.camera.y0
	window.camera.R = window.sy / 48 * (1 + tplay / 10)
	window.camera.y0 = state.Rcore - 5
	window.camera.X0 = tplay * 0.1
	background.draw(factor = 8)
	window.camera.R, window.camera.X0, window.camera.y0 = R, X0, y0
	if state.you.alive:
		state.you.draw()
	for effect in state.effects:
		effect.draw()
	background.drawwash()
	
	



