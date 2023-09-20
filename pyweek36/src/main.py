import pygame
from . import settings, view, sector
from . import scene, playscene, calibratescene
from . import ptext, pview
from .pview import T

sector.load()
view.init()
scene.current = playscene
scene.current.init()
playing = True
clock = pygame.time.Clock()
dtaccum = 0
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	kdowns = set(event.key for event in pygame.event.get(pygame.KEYDOWN))
	mdowns = set(event.button for event in pygame.event.get(pygame.MOUSEBUTTONDOWN))
	if pygame.K_ESCAPE in kdowns or pygame.event.get(pygame.QUIT, pump = True): playing = False
	if pygame.K_F10 in kdowns: view.cycle_height()
	if pygame.K_F11 in kdowns: view.toggle_fullscreen()
	if pygame.K_F12 in kdowns: pview.screenshot()
	kpressed = pygame.key.get_pressed()
	if settings.DEBUG and kpressed[pygame.K_F3]: dt *= 10
	mpos = pygame.mouse.get_pos()

	dtaccum += dt
	dt0 = 1 / settings.maxfps
	while dtaccum >= dt0:
		scene.current.think(dt0, kdowns, kpressed, mpos, mdowns)
		kdowns = set()
		mdowns = set()
		dtaccum -= dt0
	scene.current.draw()

	if settings.DEBUG:
		text = f"{clock.get_fps():.1f}fps"
		ptext.draw(text, bottomright = T(1275, 715), fontsize = T(30), owidth = 1)
	pygame.display.flip()

