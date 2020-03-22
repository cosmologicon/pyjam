import pygame
from . import settings, view, pview, scene, playscene, ptext, state, control
from .pview import T

view.init()
control.init()
pygame.display.set_caption(settings.gamename)

scene.push(playscene)

clock = pygame.time.Clock()
playing = True
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	control.think(dt)
	
	current = scene.top()
	for keys in control.get():
		if "quit" in keys:
			playing = False
		elif current:
			current.control(keys)
	if current:
		current.think(dt)
		current.draw()
	else:
		playing = False

	if settings.DEBUG:
		text = "\n".join([
			"%.1ffps" % clock.get_fps(),
			"Leaps: %d/%d" % (state.leaps, state.maxleaps),
			"thang: %.2f/%.2f" % (state.you.thang, state.thang),
		])
		ptext.draw(text, bottomleft = pview.bottomleft, fontsize = T(24), owidth = 1)
	pygame.display.flip()


