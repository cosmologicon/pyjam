import pygame
from . import settings, view, ptext, state, playscene, gameoverscene, pview
from .pview import T

settings.load()
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
			kdowns.add(event.key)
	kpressed = pygame.key.get_pressed()


	if settings.DEBUG and pygame.K_ESCAPE in kdowns:
		playing = False
	if settings.DEBUG and pygame.K_1 in kdowns:
		state.cheatwin()
	if pygame.K_F10 in kdowns:
		view.resize()
	if pygame.K_F11 in kdowns:
		view.toggle_fullscreen()
	if pygame.K_F12 in kdowns:
		pview.screenshot()


	dtaccum += dt
	dt0 = 1 / settings.maxfps
	while dtaccum > dt0:
		dtaccum -= dt0
		playscene.think(dt0, kpressed, kdowns)
	if state.gameover():
		gameoverscene.think(dt, kpressed, kdowns)

	view.clear()
	playscene.draw()
	if state.gameover():
		gameoverscene.draw()
	if settings.DEBUG:
		text = "%.1ffps" % clock.get_fps()
		ptext.draw(text, bottomleft = T(4, 716), fontsize = T(16))
	pygame.display.flip()


