import pygame
from . import settings, view, pview, playscene

view.init()
playscene.init()

playing = True
clock = pygame.time.Clock()
dtaccum = 0
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	
	kdowns = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			for k, keys in settings.controls.items():
				if event.key in keys:
					kdowns.add(k)
	if "quit" in kdowns: playing = False
	if "fullscreen" in kdowns: pview.toggle_fullscreen()
	if "resolution" in kdowns: pview.cycle_height(settings.heights)
	if "screenshot" in kdowns: pview.screenshot()
	
	kpressed0 = pygame.key.get_pressed()
	kpressed = set(k for k, keys in settings.controls.items() if any(kpressed0[key] for key in keys))

	playscene.control(kpressed)	
	dtaccum += dt
	while dtaccum >= settings.dt0:
		dtaccum -= settings.dt0
		playscene.think(settings.dt0)
	
	playscene.draw()
	pygame.display.flip()
	
	



