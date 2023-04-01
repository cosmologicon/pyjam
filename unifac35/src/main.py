import pygame, os.path
from . import settings, play, view, pview, control, state, menu, ptext, sound

ptext.FONT_NAME_TEMPLATE = os.path.join("font", "%s.ttf")
ptext.DEFAULT_FONT_NAME = "ZenDots"

sound.init()
view.init()
scene = menu
scene.init()

sound.playmusic("spy-glass")

clock = pygame.time.Clock()
playing = True
while playing:
	dt = min(clock.tick(settings.maxfps) * 0.001, 1 / settings.minfps)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			if scene is menu and event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_F1:
				if state.maxturn is not None:
					state.maxturn += 1
			if event.key == pygame.K_F10:
				pview.cycle_height(settings.heights)
			if event.key == pygame.K_F11:
				pview.toggle_fullscreen()
			if event.key == pygame.K_F12:
				pview.screenshot()
			if scene is play and event.key == pygame.K_BACKSPACE:
				play.handle("undo")
			if scene is play and event.key == pygame.K_r:
				play.handle("reset")
			if scene is play and event.key == pygame.K_ESCAPE:
				play.handle("quit")

	control.think(dt)

	scene.think(dt)
	scene.draw()
	pygame.display.flip()

