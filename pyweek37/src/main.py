import pygame
from . import settings, view, control, pview, playscene, ptext

view.init()
playscene.init()
control.init()

clock = pygame.time.Clock()
dtaccum = 0
while not control.quit and pygame.K_ESCAPE not in control.kdowns:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	if pygame.K_F12 in control.kdowns: pview.screenshot()

	playscene.think(dt)
	playscene.draw()
	
	ptext.draw(f"{clock.get_fps():.1f}fps",
		bottomleft = pview.bottomleft, fontsize = pview.T(20), owidth = 1)
	pygame.display.flip()
	


