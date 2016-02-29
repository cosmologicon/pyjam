import pygame
from . import settings, window, ptext, scene, playscene, background, quest
from .util import F

window.init()
background.init()
quest.init()
pygame.mixer.init()

scene.push(playscene)
clock = pygame.time.Clock()
playing = True

def handleevents():
	estate = {
		"mpos": pygame.mouse.get_pos(),
		"ldown": False,
		"mdown": False,
		"rdown": False,
		"lup": False,
		"mup": False,
		"rup": False,
	}
	for kname in settings.keys:
		estate[kname] = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			estate["quit"] = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F11:
				window.togglefullscreen()
			if event.key == pygame.K_F12:
				window.screenshot()
			for kname, keys in settings.keys.items():
				if event.key in keys:
					estate[kname] = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button in (1,2,3):
				estate[" lmr"[event.button] + "down"] = True
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button in (1,2,3):
				estate[" lmr"[event.button] + "up"] = True
	return estate


while playing:
	dt = 0.001 * clock.tick(settings.maxfps)
	estate = handleevents()
	if estate["quit"]:
		playing = False

	currentscene = scene.top()
	if currentscene:
		currentscene.think(dt, estate)
	window.screen.fill((0, 0, 0))
	if currentscene:
		currentscene.draw()

	if settings.DEBUG:
		ptext.draw("%.1ffps" % clock.get_fps(), bottomright = F(844, 470), fontsize = F(24))
	pygame.display.flip()

pygame.quit()

