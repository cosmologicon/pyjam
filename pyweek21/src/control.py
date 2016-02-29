import pygame
from . import state, window, state, sound, background
from .util import F

cursor = []
selection = None
assembling = False

def think(dt, estate):
	global cursor, selection, assembling
	if estate["ldown"]:
		selection = pygame.Rect(estate["mpos"], (0, 0))
	if selection is not None:
		selection.width = estate["mpos"][0] - selection.x
		selection.height = estate["mpos"][1] - selection.y
		nselect = pygame.Rect(selection)
		nselect.normalize()
		cursor[:] = [ship for ship in state.state.team if nselect.collidepoint(ship.screenpos())]
	if estate["lup"]:
		selection = None
#		building = thing.Building(pos = [x, y, 0])
#		state.state.ships[-1].setbuildtarget(building)
	if estate["rdown"]:
		from . import thing
		x, y = window.screentoworld(*estate["mpos"])
		if background.revealed(x, y):
			sound.play("go")
			for ship in cursor:
				ship.settarget((x, y))
				state.state.effects.append(thing.GoIndicator(pos = [x, y, 0]))
		else:
			sound.play("cantgo")
#	if estate["rdown"]:
#		x, y = window.screentoworld(*estate["mpos"])
#		window.targetpos(x, y)
	if estate["cycle"]:
		ship = nextcursor()
		cursor = [ship]
		window.targetpos(ship.x, ship.y, ship.z)
	if estate["assemble"]:
		assembling = True
	

def nextcursor():
	team = state.state.team
	if len(cursor) != 1:
		return team[0]
	return team[(team.index(cursor[0]) + 1) % len(team)]

def isselected(ship):
	return ship in cursor

def drawselection():
	if not selection:
		return
	rect0 = pygame.Rect(selection)
	rect0.normalize()
	d = F(2)
	rect = rect0.inflate((2 * d, 2 * d))
	box = d, d, rect0.w, rect0.h
	surf = pygame.Surface(rect.size).convert_alpha()
	surf.fill((255, 0, 255, 100))
	surf.fill((255, 0, 255, 50), box)
	window.screen.blit(surf, rect)

