import pygame
from . import settings, view, ptextgl, control

view.init()
control.init()

playing = True
clock = pygame.time.Clock()
while playing:
	dt = 0.001 * min(clock.tick(settings.maxfps), 1 / settings.minfps)
	kdowns = control.get()
	if kdowns:
		playing = False

	
	view.clear()
	ptextgl.draw("%.1ffps" % clock.get_fps(), (10, 10))
	pygame.display.flip()

pygame.quit()

