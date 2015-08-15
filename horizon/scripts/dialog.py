from __future__ import division
import pygame, math, sys, os.path, json, random
from pygame.locals import *
sys.path.insert(1, sys.path[0] + "/..")
from src import ptext, dialog

pygame.mixer.init()
clock = pygame.time.Clock()
toplay = list(dialog.lines)
dialog.sound.init()

while toplay:
	dt = clock.tick(60) * 0.001
	dialog.think(dt)
	if not dialog.queue and not dialog.sound.lineplaying():
		convo = toplay.pop(0)
		print
		print convo
		for line in dialog.lines[convo]:
			print line
		dialog.play(convo)
			
		



