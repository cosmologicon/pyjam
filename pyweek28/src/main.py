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
	mdown, mup = False, False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
			else:
				kdowns.append(event.key)
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			mdown = True
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			mup = True
	kpressed = pygame.key.get_pressed()
	mpos = pygame.mouse.get_pos()
	# TODO: get relevant mouse events and pass them to the current scene.
	
	currentscene = scene.current()
	if currentscene:
		# TODO: rewrite to use a constant framerate. Call "think" the appropriate number of times in
		# each frame.
		currentscene.think(dt, kpressed, kdowns, mpos, mdown, mup)
		currentscene.draw()
	else:
		playing = False
	if settings.DEBUG:
		pygame.display.set_caption("%s | %.1ffps" % (settings.gamename, clock.get_fps()))
		text = "\n".join([
			"Up/down: move between stations",
			"C: track car on current side of cable",
			"Left/right: change viewing angle",
			"1/2: adjust assignment at current station",
			"Q: claim quest at station with (!) icon",
			"Click on a station on right to go there",
			"Click on a person on left to reassign to a different station",
			"Esc: quit",
		])
		ptext.draw(text, fontsize = T(24), topleft = T(0, 500), owidth = 1)
	pygame.display.flip()

