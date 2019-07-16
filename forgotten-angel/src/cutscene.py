import pygame
import vista, state, button, scene, gamescene, buildscene, dialog, img, settings, sound, quest
from settings import F


buttons = []
def init():
	pass

def think(dt, events, mpos):
	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and state.state.tline > 0.5:
			dialog.advance()
	dialog.think(dt)

def draw():
	vista.screen.fill((255, 255, 255))
	dialog.draw()
	if len(state.state.playing) < 5:
		scene.pop()

