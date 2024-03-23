import pygame
from . import settings, view, control, pview, ptext, state
from . import scene, playscene, colorscene, menuscene

scene.scene = menuscene
scene.scene.init()

view.init()
control.init()

clock = pygame.time.Clock()
dtaccum = 0
while not control.quit and "quit" not in control.kdowns:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	if "resolution" in control.kdowns: view.toggleresolution()
	if "fullscreen" in control.kdowns: view.togglefullscreen()
	if "screenshot" in control.kdowns: pview.screenshot()

	scene.scene.think(dt)
	scene.scene.draw()

	ptext.draw(f"{clock.get_fps():.1f}fps",
		bottomleft = pview.bottomleft, fontsize = pview.T(20), owidth = 1)
	pygame.display.flip()

if scene.scene is playscene:
	state.save()	


