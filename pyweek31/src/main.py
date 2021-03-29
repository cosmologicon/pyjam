import pygame
from . import pview, ptext
from . import settings, state, view, hud
from . import playscene
from .pview import T

view.init()
playscene.init()

playing = True
clock = pygame.time.Clock()
dtaccum = 0
tsave = 0
while playing:
	kpressed = pygame.key.get_pressed()
	mposV = pygame.mouse.get_pos()
	events = set()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			events.add("quit")
		if event.type == pygame.KEYDOWN:
			for name, keycodes in settings.keys.items():
				if event.key in keycodes:
					events.add(name)
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				events.add("click")
			if event.button == 3:
				events.add("rclick")
			if event.button == 4:
				view.zoom(1, mposV)
			elif event.button == 5:
				view.zoom(-1, mposV)
		if event.type == pygame.MOUSEWHEEL:
			print(event)
	if "quit" in events:
		playing = False
	if "screenshot" in events:
		pview.screenshot()
	if "resize" in events:
		view.resize()
	if "fullscreen" in events:
		view.toggle_fullscreen()

	playscene.control(mposV, events)

	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	tsave += dt
	if settings.DEBUG and kpressed[pygame.K_F1]:
		dt *= 5
	dtaccum += dt

	dt0 = 1 / settings.maxfps
	while dtaccum >= dt0:
		playscene.think(dt0)
		dtaccum -= dt0

	view.clear()
	playscene.draw()

	if settings.DEBUG:
		xG, yG = view.GconvertV(mposV)
		text = "\n".join([
			"selected: %s" % hud.selected(),
			"%.1ffps" % clock.get_fps(),
			"[ %.2f, %.2f ]" % (xG, yG),
		])
		ptext.draw(text, bottomleft = T(5, pview.h0 - 5))

	pygame.display.flip()
	if settings.tautosave is not None and tsave >= settings.tautosave:
		tsave = 0
		state.save()
state.save()

