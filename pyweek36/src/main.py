import pygame
from . import settings, view, scene, playscene
from . import ptext, pview
from .pview import T

scene.current = playscene
scene.current.init()
view.init()
playing = True
clock = pygame.time.Clock()

while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	kdowns = set(event.key for event in pygame.event.get(pygame.KEYDOWN))
	if pygame.K_ESCAPE in kdowns or pygame.event.get(pygame.QUIT, pump = True): playing = False
	if pygame.K_F10 in kdowns: view.cycle_height()
	if pygame.K_F11 in kdowns: view.toggle_fullscreen()
	if pygame.K_F12 in kdowns: pview.screenshot()
	kpressed = pygame.key.get_pressed()

	scene.current.think(dt, kdowns, kpressed)
	scene.current.draw()

	text = f"{clock.get_fps():.1f}fps"
	ptext.draw(text, bottomleft = T(5, 715), fontsize = T(30), owidth = 1)
	pygame.display.flip()

