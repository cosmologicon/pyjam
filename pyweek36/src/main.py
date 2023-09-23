import pygame, os.path
from . import settings, view, sector, perform, state, progress, graphics, sound
from . import scene, playscene, calibratescene, homescene
from . import ptext, pview
from .pview import T

ptext.DEFAULT_FONT_NAME = "DaysOne"
ptext.FONT_NAME_TEMPLATE = os.path.join("fonts", "%s.ttf")
ptext.DEFAULT_LINE_HEIGHT = 0.9


sector.load()
sound.init()
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
	settings.drawbox = settings.DEBUG and kpressed[pygame.K_F2]
	dtf = 10 if settings.DEBUG and kpressed[pygame.K_F3] else 1
	if settings.DEBUG and pygame.K_F4 in kdowns:
		perform.print_report()
		graphics.print_report()
		print(state.techlevel)
	if settings.DEBUG and pygame.K_F5 in kdowns:
		progress.cheat()
	mpos = pygame.mouse.get_pos()
	#perform.print_report()

	dtaccum += dt * dtf
	dt0 = 1 / settings.maxfps * dtf
	while dtaccum >= dt0:
		scene.current.think(dt0, kdowns, kpressed, mpos, mdowns)
		kdowns = set()
		mdowns = set()
		dtaccum -= dt0
	scene.current.draw()

	if settings.DEBUG:
		text = "\n".join([
			"F2: show hit boxes",
			"F3: speed boost",
			"F4: print debug info",
			"F5: cheat",
			f"{clock.get_fps():.1f}fps",
		])
		ptext.draw(text, topright = T(1275, 5), fontsize = T(18), owidth = 1, alpha = 0.3)
	pygame.display.flip()

