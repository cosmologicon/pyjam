from __future__ import division
import pygame
from . import settings, scene, playscene, view, ptext, pview
from .pview import T

# TODO: title screen
scene.push(playscene.PlayScene())

# TODO: sound module to play music and sound effects

view.init()
clock = pygame.time.Clock()
playing = True
while playing:
	# Game time in this frame in seconds.
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	# Keys that were pressed this frame.
	kdowns = []
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
			else:
				kdowns.append(event.key)
	kpressed = pygame.key.get_pressed()
	# TODO: get relevant mouse events and pass them to the current scene.
	
	currentscene = scene.current()
	if currentscene:
		# TODO: rewrite to use a constant framerate. Call "think" the appropriate number of times in
		# each frame.
		currentscene.think(dt, kpressed, kdowns)
		currentscene.draw()
	else:
		playing = False
	if settings.DEBUG:
		pygame.display.set_caption("%s | %.1ffps" % (settings.gamename, clock.get_fps()))
		text = "\n".join([
			"Up/down: move between stations",
			"Esc: quit",
		])
		ptext.draw(text, fontsize = T(24), topleft = T(0, 0), owidth = 1.5)
	pygame.display.flip()

