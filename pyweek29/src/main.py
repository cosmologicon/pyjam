import pygame
from . import settings, view, pview, scene, playscene, ptext, state
from .pview import T

view.init()
pygame.display.set_caption(settings.gamename)

scene.push(playscene)

clock = pygame.time.Clock()
playing = True
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	kdowns = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			kdowns.add(event.key)

	if pygame.K_ESCAPE in kdowns:
		playing = False
	
	current = scene.top()
	if current:
		current.think(dt, kdowns)
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


