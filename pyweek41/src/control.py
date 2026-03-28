import pygame, math
from . import view, world, thing, settings, quest, ptext, pview

playing = True
mouseV0 = [0, 0]
dragging = False
mouseV = [0, 0]
mouseG = [0, 0]
cursor = None  # Star currently being pointed to, if any.
anchor = None  # Star selected
showinfo = True

def think(dt):
	global playing, mouseV, mouseG, cursor, anchor, mouseV0, dragging, showinfo
	ldown = False
	lup = False
	rdown = False
	wheel = 0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
			showinfo = not showinfo
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			playing = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
			view.change_res()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
			view.toggle_fullscreen()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
			view.screenshot()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
			world.advance()
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			ldown = True
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			lup = True
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			rdown = True
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
			wheel += 1
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
			wheel -= 1
	mouseV = pygame.mouse.get_pos()
	mouseG = view.GconvertV(mouseV)
	cursor = None
	if world.stars:
		nearest = min(world.stars.values(), key = lambda star: star.distanceto(mouseG))
		if nearest.distanceto(mouseG) < 2:
			cursor = nearest
			if dragging and cursor is anchor:
				cursor = None
	if ldown:
		if cursor is None:
			anchor = None
			dragging = False
		elif cursor is anchor:
			anchor = None
			dragging = False
		elif cursor is not None and anchor is None:
			anchor = cursor
			mouseV0 = mouseV
			dragging = False
		elif cursor is not None and anchor is not None:
			addlink()
	if anchor is not None and not dragging:
		dragging = math.distance(mouseV, mouseV0) > 5
	if lup:
		if dragging:
			if cursor is None or cursor is anchor:
				anchor = None
				mouseV0 = None
				dragging = False
			elif cursor is not None and anchor is not None and cursor is not anchor:
				addlink()
			else:
				print(cursor)
				print(anchor)
				raise ValueError
		dragging = False
	if rdown and settings.editor:
		if cursor is not None:
			world.removestar(cursor)
		else:
			world.addstar(mouseG)
	if rdown and not settings.editor:
		if cursor is None:
			anchor = None
			mouseV0 = None
			dragging = False
		elif anchor is None:
			cursor.removealllinks()
	if wheel != 0 and settings.editor and cursor is not None:
		world.cyclestar(cursor, wheel)

def addlink():
	global anchor, dragging, mouseV0
	link0 = anchor.haslinkto(cursor)
	if link0 is not None:
		link0.unplace()
		quest.do("remove")
		world.checkadvance()
	else:
		link = thing.Link(anchor, cursor)
		world.placelink(link)
	anchor = None
	mouseV0 = None
	dragging = False


def draw():
	if anchor is not None:
		cstar = thing.CursorStar(mouseG)
		clink = thing.CursorLink(anchor, cstar)
		clink.draw()
	pygame.mouse.set_cursor(pygame.cursors.broken_x)

	if showinfo:
		lines = [
			"Tab: hide controls/info",
			"Click and drag: link or unlink stars",
			"Right click on star: remove all links",
			"Numbers indicate how many links a star needs",
			"Y: 3 links, spaced apart (no acute angles)",
			"X: 4 links, max one X per constellation",
			"F2: cheat (advance)",
			"F10: change resolution",
			"F11: toggle fullscreen",
			"F12: screenshot",
			"Esc: quit",
		]
	else:
		lines = [
			"Tab: show controls/info",
		]
#	if settings.editor:
#		lines.append(f"{clock.get_fps():.1f}fps")
	color = math.interpI(world.sky, 1, (255, 255, 255), 5, (80, 40, 40))
	ptext.draw("\n".join(lines), bottomright = pview.T(1276, 716), fontsize = pview.T(18), color = color)



