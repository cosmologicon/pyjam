from __future__ import division
import pygame, os.path
from . import mhack, settings, view, state, ptext, quest, progress, mechanics, dialog, sound
from . import scene, playscene, menuscene, cutscene, creditscene
from .util import F

ptext.FONT_NAME_TEMPLATE = os.path.join("data", "font", "%s.ttf")
pygame.init()
view.init()
quest.init()

if settings.reset:
	state.removesave()
	progress.removesave()

if settings.quickstart:
	scene.push(playscene)
#	scene.push(menuscene)
#	scene.push(creditscene)
elif state.canload():
	scene.push(playscene)
	state.load()
elif progress.canload():
	progress.load()
	scene.push(menuscene)
else:
	scene.push(playscene)

clock = pygame.time.Clock()
playing = True
lastdown = None
while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	mpos = pygame.mouse.get_pos()
	mdown, mup, mwheel, rdown, mclick = False, False, 0, False, False
	kpressed = pygame.key.get_pressed()
	mod = any(kpressed[j] for j in (pygame.K_LSHIFT, pygame.K_LCTRL, pygame.K_RSHIFT, pygame.K_RCTRL))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if mod:
					rdown = True
				else:
					mdown = True
					lastdown = pygame.time.get_ticks(), mpos
			if event.button == 3:
				rdown = True
			if event.button == 4:
				mwheel += 1
			if event.button == 5:
				mwheel -= 1
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1 and not mod:
				mup = True
				if lastdown is not None:
					t0, (x0, y0) = lastdown
					tclick = (pygame.time.get_ticks() - t0) * 0.001
					dx, dy = mpos[0] - x0, mpos[1] - y0
					if tclick < mechanics.tclick and abs(dx) < mechanics.dclick > abs(dy):
						mclick = True
				lastdown = None
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_1:
				mwheel -= 4
			if event.key == pygame.K_2:
				mwheel += 4
			if event.key == pygame.K_TAB:
				dialog.abort()
			if event.key == pygame.K_SPACE:
				dialog.skip()
			if event.key == pygame.K_ESCAPE:
				playing = False
			if event.key == pygame.K_F11:
				view.togglefullscreen()
			if event.key == pygame.K_F12:
				view.screenshot()
			if event.key == pygame.K_F2:
				state.win()
			if event.key == pygame.K_F3:
				state.cheat()
			if event.key == pygame.K_F4:
				progress.beatone()
			if event.key == pygame.K_F5:
				state.lose()

	if kpressed[pygame.K_F1]:
		dt *= 10

	s = scene.top()
	s.think(dt, mpos, mdown, mup, mwheel, rdown, mclick)
	sound.think(dt)
	s.draw()
	if not playing:
		s.abort()

	if settings.showfps:
		ptext.draw("%.1ffps" % clock.get_fps(),
			right = F(844), top = F(250), fontsize = F(26), color = "yellow")

	pygame.display.flip()
pygame.quit()
