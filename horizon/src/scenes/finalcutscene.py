from __future__ import division
import pygame, math, random, time
from pygame.locals import *
from src import window, thing, settings, state, hud, quest, background, dialog, sound
from src.window import F

def init():
	global tplay, tspawn

	window.camera.X0 = 0
	window.camera.y0 = 500
	window.camera.R = window.sy / 40
	sound.epicness = 2
	dialog.play("finale")
	tplay = 0
	background.wash()
	state.you = getattr(thing, quest.quests["Finale"].winner)(X = 0, y = window.camera.y0 + 20)
	state.effects = []
	frange = lambda x, y, a = 1.0: [n * a for n in range(int(x / a), int(y / a))]
	tspawn = frange(12, 30, 2) + frange(14.5, 30, 1.11) + frange(19.27, 30, 0.28)
	tspawn.sort()

def think(dt, events, kpressed):
	global todraw, tplay
	dialog.think(dt)
	background.think(dt, 2)
	sound.think(dt)

	tplay += dt

	state.you.y -= 1 * dt
	if tplay > 7 and state.you.alive:
		state.you.die()
		state.effects.append(
			thing.CutsceneTeleport(X = 0, y = state.you.y, X1 = 0, y1 = window.camera.y0 - 20, color = "gray")
		)
	while tspawn and tplay > tspawn[0]:
		tspawn.pop(0)
		state.effects.append(thing.CutsceneTeleport(
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
	class camera:
		R = window.sy / 48 * (1 + tplay / 10)
		y0 = state.Rcore - 5
		X0 = tplay * 0.1
	background.draw(factor = min(settings.backgroundfactor, 8), camera = camera, hradius = -1)
	background.drawwash()
	if state.you.alive:
		state.you.draw()
	for effect in state.effects:
		effect.draw()
	background.drawwash()
	
