from __future__ import division
import pygame, math, random, time
from pygame.locals import *
from src import window, thing, settings, state, hud, quest, background, dialog, ptext, scene
from src.scenes import play
from src.window import F


R = 16 * state.R  # Draw the horizon larger for the title shot
y0 = R + 400

control = {}

def init():
	global t
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

def think(dt, events, kpressed):
	global t
	t += dt

	hud.think(dt)
	quest.think(dt)
	dialog.think(dt)
	background.flowt += 4 * dt

	for event in (events or []):
		if event.type == KEYUP and event.key == "go" and t > 6:
			scene.current = play
		
	for ship in state.ships:
		ship.think(dt)
	for effect in state.effects:
		effect.think(dt)
	state.effects = [e for e in state.effects if e.alive]


	dt = max(dt, 0.1)
	window.camera.X0 = 0
	window.camera.y0 += (1 - math.exp(-0 * dt)) * (R - window.camera.y0)
	
	Rwin = window.sy / 1600
	window.camera.R += (1 - math.exp(-0.3 * dt)) * (Rwin - window.camera.R)
	
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

	for ship in state.ships:
		ship.draw()
	for effect in state.effects:
		effect.draw()
	px, py = window.screenpos(0, 0)
#	r = int(window.camera.R * R)
#	if py - r < window.sy:
#		pygame.draw.circle(window.screen, (0, 40, 20), (px, py), r)
	dialog.draw()
	a1 = math.clamp((t - 4) / 2, 0, 1)
	a2 = math.clamp((t - 6) / 2, 0, 1)
	ptext.draw(settings.gamename, fontsize = F(70), center = F(427, 200),
		owidth = 2, color = "#AAFFCC", alpha = a1, fontname = "Audiowide")
	ptext.draw("by Christopher Night", fontsize = F(32), midtop = F(427, 250),
		owidth = 1, color = "gray", alpha = a2, fontname = "Audiowide")
#	ptext.draw("music: Mary Bichner", fontsize = F(32), midtop = F(220, 290),
#		owidth = 1, color = "gray")
#	ptext.draw("testing: ???", fontsize = F(32), midtop = F(220, 340),
#		owidth = 1, color = "gray")
#	ptext.draw("production: ???", fontsize = F(32), midtop = F(854-220, 290),
#		owidth = 1, color = "gray")


