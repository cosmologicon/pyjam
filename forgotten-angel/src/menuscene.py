import pygame
from . import vista, state, button, scene, gamescene, cutscene, buildscene, dialog, img, settings, sound, quest
from .settings import F


buttons = []
def init():
	global buttons
	buttons = [
		button.Button("Continue" if state.canload() else "New Game", F(854/2 - 90, 300, 180, 30), fontsize = F(22)),
		button.Button("Quit", F(854/2 - 90, 350, 180, 30), fontsize = F(22)),
	]

def think(dt, events, mpos):
	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if buttons[0].within(mpos):
				play()
			if buttons[1].within(mpos):
				quit()
	sound.playmusic("title")

def draw():
	vista.screen.fill((255, 255, 255))
	img.drawtext(settings.gamename, F(60), center = F(854/2, 120), fontname = "prosto")
	img.drawtext("by Christoper Night\n ", F(20), center = F(854/2, 220), fontname = "prosto")
	img.drawtext("music by Mary Bichner\n ", F(20), center = F(854/2, 270), fontname = "prosto")
	for b in buttons:
		b.draw()

def play():
	if state.canload():
		state.load()
		scene.pop()
		scene.push(gamescene)
		scene.push(buildscene)
	else:
		state.reset()
		scene.pop()
		scene.push(gamescene)
		scene.push(cutscene)

def quit():
	scene.pop()

