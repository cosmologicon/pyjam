import pygame
from . import settings, pview, scene, playscene

# TODO: add background music

pview.set_mode(settings.size0)
pygame.display.set_caption(settings.gamename)

# TODO: start with a splash screen that just shows the title and team name.
# This can be a different scene object, and when you press a key it pushes
# playscene on.
scene.push(playscene.PlayScene())

playing = True
clock = pygame.time.Clock()
while playing:
	dt = 0.001 * clock.tick()
	kdowns = [] # keys pressed this frame
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				playing = False
			elif event.key == pygame.K_F10:
				pview.toggle_fullscreen()
			elif event.key == pygame.K_F11:
				pview.cycle_height(settings.heights)
			elif event.key == pygame.K_F12:
				pview.screenshot()
			else:
				kdowns.append(event.key)
	kpressed = pygame.key.get_pressed()
	currentscene = scene.top()
	if currentscene:
		currentscene.think(dt, kdowns, kpressed)
		currentscene.draw()
	pygame.display.flip()

pygame.quit()

