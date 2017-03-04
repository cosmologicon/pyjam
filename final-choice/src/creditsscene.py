import math, random, pygame
from pygame.locals import *
from . import view, state, thing, background, settings, hud, util, sound, image, ptext, scene, settings
from .pview import T

class self:
	pass

def init():
	sound.mplay(3 if state.best else 2)
	self.t = 0

def think(dt, kdowns, kpressed):
	self.t += dt
	if self.t >= 45:
		scene.quit()

def draw():
	background.drawfly()
	for jline, line in enumerate(lines):
		dj = 0.5 if jline >= len(lines) - 2 else jline % 2
		tline = line[0]
		dt = self.t - tline
		if not 0 <= dt <= 6:
			continue
		alpha = util.clamp(min(1.5 * dt, 1.5 * (5 - dt)), 0, 1)
		pos = T(240, 300 + 300 * dj) if settings.portrait else T(240 + 400 * dj, 200 + 60 * dj)
		ptext.draw(line[1], midbottom = pos, color = (200, 255, 255), fontname = "Bungee", fontsize = T(26), alpha = alpha)

		dt -= 0.1
		alpha = util.clamp(min(1.5 * dt, 1.5 * (5 - dt)), 0, 1)
		names = "\n".join(line[2:])
		ptext.draw(names, midtop = pos, color = (255, 255, 255), fontname = "Bungee", fontsize = T(26), alpha = alpha)


lines = [
	[2, "Team Lead", "Christopher Night"],
	[3, "Programming", "Christopher Night"],
	[8, "Game Concept", "Charles McPillan"],
	[9, "Story Lead", "Magnus Drebenstedt"],
	[14, "Music", "Mary Bichner"],
	[15, "Production", "Charles McPillan"],
	[20, "Voices", "Randy Parcel", "Jules Van Oosterom", "Adam Jones", "Mary Bichner", "Charles McPillan"],
	[21, "Graphics", "Christopher Night"],
	[26, "Character and\nBackground Art", "Many contributors\nat Pixabay"],
	[27, "Sound Effects", "Christopher Night"],
	[32, '"The Ballad of Captain Alyx"', "Music by Mary Bichner", "Lyrics by Christopher Night"],
	[38, settings.gamename, "by Team Universe Factory", "for PyWeek 23"],
]

