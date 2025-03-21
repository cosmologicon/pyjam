import pygame, math, random
from . import state, window, state, sound, background, settings, dialogue, util
from .util import F

cursor = []
selection = None
assembling = False
tclick = 0
dragged = False
lastclick = None
mdrag = None

def think(dt, estate):
	global cursor, selection, assembling, tclick, dragged, oldcursor, lastclick, mdrag
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
			oldcursor = list(cursor)
		if dragged:
			ships = [ship for ship in state.state.team if nselect.collidepoint(ship.selectrect().center)]
			if estate["iskmulti"]:
				for ship in ships:
					if ship not in cursor:
						cursor.append(ship)
			else:
				cursor = ships
	if estate["lup"]:
		if dragged:
			if cursor:
				ships = [ship for ship in cursor if ship not in oldcursor]
				if len(ships) == 1:
					selectack(ships[0])
		else:
			newcursor = None
			avatarrects = [pygame.Rect(F(4 + 64 * j, 4, 60, 60)) for j in range(len(state.state.team))]
			up1rects = [pygame.Rect(F(4 + 64 * j, 68, 28, 28)) for j in range(len(state.state.team))]
			up2rects = [pygame.Rect(F(34 + 64 * j, 68, 28, 28)) for j in range(len(state.state.team))]
			clicked = False
			clickedhud = False
			if background.minimaprect().collidepoint(estate["mpos"]):
				estate["map"] = True
				clicked = True
				clickedhud = True
			for r, u1, u2, ship in zip(avatarrects, up1rects, up2rects, state.state.team):
				if r.collidepoint(estate["mpos"]):
					t = pygame.time.get_ticks() * 0.001
					if lastclick is not None and t - lastclick < settings.doubleclicktime:
						newcursor = list(state.state.team)
					else:
						newcursor = [ship]
					lastclick = t
					clicked = True
					clickedhud = True
				if u1.collidepoint(estate["mpos"]):
					clicked = True
					clickedhud = True
					if state.state.bank >= ship.up1cost():
						state.state.bank -= ship.up1cost()
						ship.up1()
						sound.play("buy")
					else:
						sound.play("cantbuy")
				if u2.collidepoint(estate["mpos"]):
					clicked = True
					clickedhud = True
					if state.state.bank >= ship.up2cost():
						state.state.bank -= ship.up2cost()
						ship.up2()
						sound.play("buy")
					else:
						sound.play("cantbuy")
			if not clicked:
				clicks = [ship for ship in state.state.team if ship.selectrect().collidepoint(estate["mpos"])]
				if clicks:
					t = pygame.time.get_ticks() * 0.001
					if lastclick is not None and t - lastclick < settings.doubleclicktime:
						newcursor = list(state.state.team)
					else:
						ship = min(clicks, key = lambda ship: ship.y)
						newcursor = [ship]
					lastclick = t
					clicked = True
			# click on the HUD but didn't select a new character
			if clickedhud and not newcursor:
				pass
			# selected a character from the HUD
			elif clickedhud and newcursor:
				if estate["iskmulti"]:
					if newcursor[0] in cursor:
						cursor.remove(newcursor[0])
					else:
						cursor.append(newcursor[0])
						selectack(newcursor[0].letter)
				else:
					cursor = newcursor
					selectack(cursor[0].letter)
			# clicked on a character in the gameplay area
			elif clicked and not clickedhud:
				# TODO: check for double click
				if estate["iskmulti"]:
					if newcursor[0] in cursor:
						cursor.remove(newcursor[0])
					else:
						cursor.append(newcursor[0])
						selectack(newcursor[0].letter)
				else:
					cursor = newcursor
					selectack(cursor[0].letter)
			# clicked on nothing
			else:
				if not estate["iskmulti"]:
					cursor = []

		selection = None
	if estate["rdown"]:
		from . import thing
		x, y = window.screentoworld(*estate["mpos"])
#		if background.revealed(x, y) and background.island(x, y):
		if cursor:
			if dialogue.tquiet > 0.5:
				sound.play("dialogue/ACK" + random.choice(cursor).letter + random.choice("23"))
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
	if estate["mdown"]:
		mdrag = estate["mpos"]
	if mdrag is not None:
		dx = estate["mpos"][0] - mdrag[0]
		dy = estate["mpos"][1] - mdrag[1]
		mdrag = estate["mpos"]
		window.scoot(-dx / (window.Z * util.f), dy / (window.Z * util.f * window.fy))
	if estate["mup"]:
		mdrag = None
	if estate["cycle"]:
		ship = nextcursor()
		selectack(ship.letter)
		cursor = [ship]
#		window.targetpos(ship.x, ship.y, ship.z)
	if estate["issnap"] and cursor:
		ship = cursor[0]
		window.targetpos(ship.x, ship.y, ship.z)
	if settings.DEBUG and estate["assemble"]:
		assemble(window.x0, window.y0)

def assemble(x, y):
	global assembling
	assembling = x, y
	

def selectack(letter):
	if dialogue.tquiet > 0.5:
		sound.play("dialogue/ACK%s1" % letter)

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
			avoided = True
			if dx or dy:
				d = math.sqrt(dx ** 2 + dy ** 2)
				tx = building.x + dx * R / d
				ty = building.y + dy * R / d
			else:
				ty -= R
			ship.settarget((tx, ty))
	return avoided

