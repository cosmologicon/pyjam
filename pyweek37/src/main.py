import pygame
from . import settings, view, control, pview, ptext
from . import scene, playscene, colorscene, menuscene

scene.scene = menuscene
scene.scene.init()

view.init()
control.init()

clock = pygame.time.Clock()
dtaccum = 0
while not control.quit and pygame.K_ESCAPE not in control.kdowns:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	if pygame.K_F12 in control.kdowns: pview.screenshot()

	scene.scene.think(dt)
	scene.scene.draw()

	ptext.draw(f"{clock.get_fps():.1f}fps",
		bottomleft = pview.bottomleft, fontsize = pview.T(20), owidth = 1)
	pygame.display.flip()
	


