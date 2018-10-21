import pygame
from pygame.locals import *
from . import maff, settings, view, scene, gamescene, graphics

view.init()
graphics.init()
scene.push(gamescene)

playing = True
clock = pygame.time.Clock()
while playing:
	dt = clock.tick(settings.maxfps) * 0.001
	kdowns = set()
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			kdowns.add(event.key)
		if event.type == QUIT:
			playing = False
	kpressed = pygame.key.get_pressed()
	pressed = { key: any(kpressed[code] for code in codes) for key, codes in settings.keymap.items() }
	downs = { key: any(code in kdowns for code in codes) for key, codes in settings.keymap.items() }
	if downs["quit"]:
		playing = False
	s = scene.top()
	if s is None:
		break
	s.think(dt, pressed, downs)
	s.draw()
	if settings.DEBUG:
		text = "%s: %.1ffps" % (settings.gamename, clock.get_fps())
		pygame.display.set_caption(text)
	pygame.display.flip()
	if K_F12 in kdowns:
		view.screenshot()
pygame.quit()
