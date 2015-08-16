from __future__ import division
import pygame, math, random, time
from pygame.locals import *
from src import window, thing, settings, state, hud, quest, background, dialog, ptext, scene, sound
from src.scenes import play
from src.window import F


R = 16 * state.R  # Draw the horizon larger for the title shot
y0 = R + 400

control = {}

t = 0
def init():
	global t, Rfactor
	t = 0

	dy = y0 - window.camera.y0
	dX = window.camera.y0 / y0
	for ship in state.ships:
		ship.X *= dX
		ship.y += dy
	for effect in state.effects:
		effect.X *= dX
		effect.y += dy
	window.camera.y0 = y0
	window.camera.X0 = 0
	sound.playtitlemusic()
	Rfactor = window.camera.R / window.sy

def think(dt, events, kpressed):
	global t, Rfactor
	t += dt

	hud.think(dt)
	quest.think(dt)
	dialog.think(dt)
	background.flowt += 4 * dt

	for event in (events or []):
		if event.type == KEYUP and event.key == "go" and t > 8:
			scene.current = play
			scene.toinit = play
			background.wash()
		
	for ship in state.ships:
		ship.think(dt)
	for effect in state.effects:
		effect.think(dt)
	state.effects = [e for e in state.effects if e.alive]


	dt = max(dt, 0.1)
	window.camera.X0 = 0
	factor = 0.005 * t
	window.camera.y0 += (1 - math.exp(-factor * dt)) * (R - 300 - window.camera.y0)
	
	Rfactor += (1 - math.exp(-0.3 * dt)) * (1 / 1600 - Rfactor)
	window.camera.R = window.sy * Rfactor

def draw():
	window.screen.fill((0, 0, 0))
	if t < 1.5:
		background.drawstars()
		surf = window.screen.copy().convert_alpha()
		surf.fill((0, 0, 0, int(255 * t / 1.5)))
		window.screen.blit(surf, (0, 0))
	else:
		window.camera.y0 /= R / state.R
		window.camera.R *= 2.5
		background.draw()
		window.camera.y0 *= R / state.R
		window.camera.R /= 2.5

	if t < 5:
		for ship in state.ships:
			ship.draw()
	px, py = window.screenpos(0, 0)
#	r = int(window.camera.R * R)
#	if py - r < window.sy:
#		pygame.draw.circle(window.screen, (0, 40, 20), (px, py), r)
	dialog.draw()
	drawtitle()

def drawtitle():
	a1 = math.clamp((t - 4) / 2, 0, 1)
	a2 = math.clamp((t - 5.5) / 2, 0, 1)
	a3 = math.clamp((t - 6.5) / 2, 0, 1)
	a4 = math.clamp((t - 8) / 2, 0, 1)
	ptext.draw(settings.gamename, fontsize = F(70), center = F(427, 140),
		owidth = 2, color = "#44FF77", gcolor = "#AAFFCC", alpha = a1, fontname = "Audiowide")
	ptext.draw("by Christopher Night", fontsize = F(26), midtop = F(427, 180),
		owidth = 2, color = "#7777FF", gcolor = "#AAAAFF", alpha = a2, fontname = "Audiowide")
	ptext.draw("MUSIC\nPRODUCTION\nTESTING\nARTWORK\nVOICE",
		fontsize = F(24), topright = F(427 - 10, 240), lineheight = 1.24,
		owidth = 2, color = "#7777FF", gcolor = "#AAAAFF", alpha = a2, fontname = "Audiowide")
	ptext.draw("Mary Bichner\nCharles McPillan\nLeo Stein\nMolly Zenobia\nRandy Parcel",
		fontsize = F(24), topleft = F(427 + 10, 240), lineheight = 1.24,
		owidth = 2, color = "#7777FF", gcolor = "#AAAAFF", alpha = a2, fontname = "Audiowide")
	ptext.draw("Press space to begin",
		fontsize = F(24), midtop = F(427, 440),
		owidth = 2, color = "#777777", gcolor = "#AAAAAA", alpha = a3, fontname = "Audiowide")


