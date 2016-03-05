import pygame, math
from . import state, window, state, sound, background, settings
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
#		if background.revealed(x, y) and background.island(x, y):
		if True:
			sound.play("go")
			for ship in cursor:
				ship.settarget((x, y))
			resolvetargets(x, y)
			for ship in cursor:
				state.state.effects.append(thing.GoIndicator(pos = [ship.target[0], ship.target[1], 0]))
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

# Make sure that all ships are moving to places where they won't pile up, and also won't be on top
# of buildings. This may mean moving some ships that are not already moving.
def resolvetargets(tx, ty):
	separateships(tx, ty)
	if avoidbuildings():
		separateships(tx, ty)
		avoidbuildings()
def vpos(ship):
	return ship.target or (ship.x, ship.y)
def swithin(ship, tx, ty):
	sx, sy = vpos(ship)
	return (sx - tx) ** 2 + (sy - ty) ** 2 < settings.shipspacing ** 2
def separateships(tx, ty):
	ships = [ship for ship in state.state.team if swithin(ship, tx, ty)]
	if len(ships) <= 1:
		return False
	R = settings.shipspacing / (2 * math.sin(math.pi / len(ships)))  # polygon circumradius
	xs, ys = zip(*map(vpos, ships))
	x0, y0 = sum(xs) / len(xs), sum(ys) / len(ys)
	ds = [(x - x0, y - y0) for x, y in zip(xs, ys)]
	angles = [math.atan2(dx, dy) if (dx or dy) else 0 for dx, dy in ds]
	# ... pick angles better?
	angles = [1 + 2 * math.pi * j / len(ships) for j in range(len(ships))]
	print len(ships), angles
	for ship, angle in zip(ships, angles):
		x = tx + R * math.sin(angle)
		y = ty + R * math.cos(angle)
		ship.settarget((x, y))
	return True
def avoidbuildings():
	avoided = False
	R = settings.buildingspacing
	for ship in state.state.team:
		if not ship.target:
			continue
		tx, ty = ship.target
		for building in state.state.buildingsnear(tx, ty):
			dx, dy = tx - building.x, ty - building.y
			if dx ** 2 + dy ** 2 > R ** 2:
				continue
			print dx, dy, R
			avoided = True
			if dx or dy:
				d = math.sqrt(dx ** 2 + dy ** 2)
				tx = building.x + dx * R / d
				ty = building.y + dy * R / d
			else:
				ty -= R
			ship.settarget((tx, ty))
	return avoided

