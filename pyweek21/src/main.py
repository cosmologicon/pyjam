from __future__ import division
import pygame, os
from . import settings, window, ptext, background, quest, control, state, dialogue
from . import scene, playscene, crawlscene
from .util import F

ptext.FONT_NAME_TEMPLATE = "data/fonts/%s.ttf"
window.init()
background.init()
quest.init()
pygame.mixer.init()

if settings.restart:
	state.deletesave()
if os.path.exists(settings.savename):
	state.load()
	scene.push(playscene)
else:
	if settings.DEBUG:
		scene.push(playscene)
	else:
		scene.push(crawlscene)
clock = pygame.time.Clock()
playing = True

def handleevents():
	estate = {
		"mpos": pygame.mouse.get_pos(),
		"ldown": False,
		"mdown": False,
		"rdown": False,
		"lup": False,
		"mup": False,
		"rup": False,
	}
	kpressed = pygame.key.get_pressed()
	for kname, keys in settings.keys.items():
		estate[kname] = False
		estate["is" + kname] = any(kpressed[key] for key in keys)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			estate["quit"] = True
		if event.type == pygame.KEYDOWN:
			if event.key in (pygame.K_F11, pygame.K_f):
				window.togglefullscreen()
			if event.key == pygame.K_F12:
				window.screenshot()
			if settings.DEBUG and event.key == pygame.K_F1:
				jumptop()
			if settings.DEBUG and event.key == pygame.K_F2:
				jumptoq()
			if settings.DEBUG and event.key == pygame.K_F3:
				jumptor()
			if settings.DEBUG and event.key == pygame.K_F4:
				jumptos()
			if settings.DEBUG and event.key == pygame.K_F5:
				jumptox()
			if settings.DEBUG and event.key == pygame.K_F6:
				jumptox2()
			if settings.DEBUG and event.key == pygame.K_F7:
				state.state.bank += 100
			if settings.DEBUG and event.key == pygame.K_F8:
				dialogue.clear()
			if settings.DEBUG and event.key == pygame.K_F10:
				state.save()
			for kname, keys in settings.keys.items():
				if event.key in keys:
					estate[kname] = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button in (1,2,3):
				estate[" lmr"[event.button] + "down"] = True
		if event.type == pygame.MOUSEBUTTONUP:
			if event.button in (1,2,3):
				estate[" lmr"[event.button] + "up"] = True
	return estate

def jumptox():
	background.revealall()
	unlockentireteam()
	obj = quest.quests["act3"].objective
	x, y = obj.x, obj.y
	control.assemble(x + 25, y + 25)

def jumptox2():
	quest.quests["act3"].progress = 6
	quest.quests["act3"].startpart1()
#	quest.quests["act3"].playpart1(0)
	quest.quests["act3"].startpart2()

def unlockcoreteam():
	for ship in state.state.ships:
		if ship not in state.state.team and len(state.state.team) < 3:
			state.state.addtoteam(ship)

def unlockentireteam():
	for ship in state.state.ships + [quest.quests["obj" + a].ship for a in "qrs"]:
		if ship not in state.state.team:
			state.state.addtoteam(ship)

def jumptop():
	obj = quest.quests["objp"].towers[0]
	x, y = obj.x, obj.y
	background.reveal(x, y, 160)
	unlockcoreteam()
	control.assemble(x + 25, y + 25)

def jumptoq():
	obj = quest.quests["objq"].towers[0]
	x, y = obj.x, obj.y
	background.reveal(x, y, 160)
	unlockcoreteam()
	control.assemble(x + 25, y + 25)

def jumptor():
	obj = quest.quests["objr"].towers[0]
	x, y = obj.x, obj.y
	background.reveal(x, y, 200)
	unlockcoreteam()
	control.assemble(x + 25, y + 25)

def jumptos():
	for obj in quest.quests["objs"].towers:
		x, y = obj.x, obj.y
		background.reveal(x, y, 160)
	unlockcoreteam()
	control.assemble(x + 25, y + 25)

while playing:
	dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
	estate = handleevents()
	if estate["quit"]:
		playing = False

	currentscene = scene.top()
	if currentscene:
		currentscene.think(dt, estate)
	window.screen.fill((0, 0, 0))
	if currentscene:
		currentscene.draw()

	if settings.DEBUG:
		ptext.draw("%.1ffps" % clock.get_fps(), bottomright = F(844, 470), fontsize = F(24))
	pygame.display.flip()

pygame.quit()

