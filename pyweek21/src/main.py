import pygame
from . import settings, window, ptext, scene, playscene, background, quest, control, state
from .util import F

window.init()
background.init()
quest.init()
pygame.mixer.init()

scene.push(playscene)
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
			if event.key == pygame.K_F11:
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
	obj = quest.quests["act3"].objective
	for ship in state.state.ships:
		if ship not in state.state.team:
			state.state.addtoteam(ship)
	x, y = obj.x, obj.y
	control.assemble(x + 25, y + 25)
	
def jumptop():
	background.revealall()
	obj = quest.quests["objp"].towers[0]
	x, y = obj.x, obj.y
	for ship in state.state.ships:
		if ship not in state.state.team and len(state.state.team) < 3:
			state.state.addtoteam(ship)
	control.assemble(x + 25, y + 25)


while playing:
	dt = 0.001 * clock.tick(settings.maxfps)
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

