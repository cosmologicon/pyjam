import pygame
from . import settings, view, ptext, state, pview
from . import scene, playscene, gameoverscene, menuscene
from .pview import T

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
ptext.DEFAULT_FONT_NAME = "berkshire"
settings.load()
view.init()

scene.current = "menu"
menuscene.init()

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
	if settings.DEBUG and pygame.K_2 in kdowns:
		state.cheatgrow()
	if pygame.K_F10 in kdowns:
		view.resize()
	if pygame.K_F11 in kdowns:
		view.toggle_fullscreen()
	if pygame.K_F12 in kdowns:
		pview.screenshot()
	current = scene.current


	dtaccum += dt
	dt0 = 1 / settings.maxfps
	while dtaccum > dt0:
		dtaccum -= dt0
		if current in ["adventure", "endless"]:
			playscene.think(dt0, kpressed, kdowns)
	if current == "gameover":
		gameoverscene.think(dt, kpressed, kdowns)
	if current == "menu":
		menuscene.think(dt, kpressed, kdowns)

	view.clear()

	if current == "menu":
		menuscene.draw()
	if current in ["adventure", "endless"]:
		playscene.draw()
	if current == "gameover":
		gameoverscene.draw()
	if settings.DEBUG:
		text = "\n".join([
			"%.1ffps" % clock.get_fps(),
			"1: beat current",
			"2: grow",
		])
		ptext.draw(text, bottomleft = T(4, 716), fontsize = T(16))
	pygame.display.flip()


