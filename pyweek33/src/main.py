import pygame
from . import settings, pview, view, ptext
from . import playscene
from .pview import T


view.init()

playscene.init()
scene = playscene

playing = True
dtaccum = 0
clock = pygame.time.Clock()
while playing:
	dt0 = 1 / settings.maxfps
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	dtaccum += dt
	kdowns = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN:
			kdowns.add(settings.keys_by_code.get(event.key))
	if "quit" in kdowns:
		playing = False

	kpressed = pygame.key.get_pressed()
	kpressed = { key: any(kpressed[code] for code in codes) for key, codes in settings.keys.items() }
	kdx = dt * (kpressed["right"] - kpressed["left"])
	kdy = dt * (kpressed["up"] - kpressed["down"])
	scene.control(kdowns, kdx, kdy)
	
	while dtaccum > 0:
		scene.think(dt0)
		dtaccum -= dt0
	scene.draw()
	
	if settings.DEBUG:
		text = "\n".join([
			"%.1ffps" % clock.get_fps(),
		])
		ptext.draw(text, fontsize = T(30), owidth = T(2), bottomleft = T(0, 720))

	pygame.display.flip()


