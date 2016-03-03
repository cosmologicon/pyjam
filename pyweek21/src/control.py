import pygame, math
from . import state, window, state, sound, background
from .util import F

cursor = []
selection = None
assembling = False
tclick = 0
dragged = False

def think(dt, estate):
	global cursor, selection, assembling, tclick, dragged
	if estate["ldown"]:
		selection = pygame.Rect(estate["mpos"], (0, 0))
		tclick = 0
		dragged = False
	if selection is not None:
		tclick += dt
		selection.width = estate["mpos"][0] - selection.x
		selection.height = estate["mpos"][1] - selection.y
		nselect = pygame.Rect(selection)
		nselect.normalize()
		if nselect.width > 5 or nselect.height > 5 or tclick > 0.5:
			dragged = True
		if dragged:
			cursor[:] = [ship for ship in state.state.team if nselect.collidepoint(ship.screenpos())]
	if estate["lup"]:
		selection = None
		if not dragged:
			if background.minimaprect().collidepoint(estate["mpos"]):
				estate["map"] = True
#		building = thing.Building(pos = [x, y, 0])
#		state.state.ships[-1].setbuildtarget(building)
	if estate["rdown"]:
		from . import thing
		x, y = window.screentoworld(*estate["mpos"])
		if background.revealed(x, y) and background.island(x, y):
			sound.play("go")
			for ship in cursor:
				r = 8
				for building in state.state.buildings:
					dx = x - building.x
					dy = y - building.y
					if dx ** 2 + dy ** 2 > r ** 2:
						continue
					if not dx and not dy:
						x += r
					else:
						d = math.sqrt(dx ** 2 + dy ** 2)
						x += r / d * dx
						y += r / d * dy
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
#		window.targetpos(ship.x, ship.y, ship.z)
	if estate["snap"] and cursor:
		ship = cursor[0]
		window.targetpos(ship.x, ship.y, ship.z)
	if estate["assemble"]:
		assemble(window.x0, window.y0)

def assemble(x, y):
	global assembling
	assembling = x, y
	

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

