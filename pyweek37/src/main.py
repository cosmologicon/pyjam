import pygame
from . import settings, view, control, pview, ptext, state, sound
from . import scene, playscene, colorscene, menuscene

sound.init()
scene.scene = menuscene
scene.scene.init()

view.init()
control.init()

clock = pygame.time.Clock()
dtaccum = 0
while not control.quit:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	if "resolution" in control.kdowns: view.toggleresolution()
	if "fullscreen" in control.kdowns: view.togglefullscreen()
	if "screenshot" in control.kdowns: pview.screenshot()
	if "quit" in control.kdowns:
		if scene.scene is playscene:
			state.save()
			scene.scene = menuscene
			scene.scene.init()
		else:
			break

	scene.scene.think(dt)
	scene.scene.draw()

	if settings.DEBUG:
		ptext.draw(f"{clock.get_fps():.1f}fps",
			bottomleft = pview.bottomleft, fontsize = pview.T(40), owidth = 1)
	pygame.display.flip()

if scene.scene is playscene:
	state.save()


