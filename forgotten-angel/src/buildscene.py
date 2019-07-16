from __future__ import division
import pygame, random
import vista, state, scene, settings, img, parts, dialog, button, sound, gamescene
from settings import F

controls = []
cps = []
cursor = None
mpos = None
buttons = []

# modules
mx0, my0, mscale = F(20, 80, 40)

# board
bx0, by0, bscale = F(854/2 - settings.shipw * 60 / 2, 100, 60)
brect = pygame.Rect((bx0, by0, bscale * settings.shipw, bscale * settings.shiph))

# conduits
cx0, cy0, cscale, csep = 600, 100, 50, 60


def init():
	global controls, cursor, point, cps
	controls = [
		parts.Conduit((1,)),
		parts.Conduit((2,)),
		parts.Conduit((3,)),
		parts.Conduit((1,2,)),
		parts.Conduit((1,3,)),
		parts.Conduit((2,3,)),
	]
	cps = [
		F(854 - 130 + 90 * (j % 3 - 1) - 25, 80 + 100 * (j // 3), 50)
		for j in range(len(controls))
	]

	del buttons[:]
	buttons.append(button.Button("Remove All", F(720, 390, 120, 30), fontsize = F(22)))
	buttons.append(button.Button("Depart", F(720, 430, 120, 30), fontsize = F(22)))
	buttons.extend(
		button.Button("buy" + s, (x - F(15), y + F(55), F(80), F(40)), fontsize = F(14))
		for (x, y, _), s in zip(cps, "1 2 3 12 13 23".split())
	)
	for j, modulename in enumerate(state.state.available):
		controls.append(parts.Module(modulename))
		cps.append((mx0 + F(85) * (j // 4), my0 + F(85) * (j % 4), mscale))
	cursor = None
	point = None
	gamescene.setshroud((0,0,0))
	state.state.you.hp = state.state.you.maxhp
	state.save()

# can be: a tuple on the board, a button name, or a module or conduit
def pointat((mx, my)):
	if brect.collidepoint((mx, my)):
		return (mx - bx0) / bscale, (my - by0) / bscale
	for button in buttons:
		if button.within((mx, my)):
			return button.name
	for control, (x0, y0, b) in zip(controls, cps):
		x = (mx - x0) / b
		y = (my - y0) / b
		if control.contains((x, y)):
			return control
	return None

def handleclick():
	global cursor
	if isinstance(point, tuple):
		if cursor:
			icon = cursor.nearest(point)
			if state.state.canaddpart(icon):
				state.state.addpart(icon)
				sound.play("build")
				cursor = None
			else:
				sound.play("cantbuild")
		else:
			part = state.state.partat(map(int, point))
			if part:
				state.state.removepart(part)
				sound.play("unbuild")
	elif isinstance(point, basestring):
		if point == "Remove All":
			state.state.removeall()
			sound.play("unbuild")
		elif point == "Depart" and state.state.cango():
			scene.pop()
			gamescene.makebuttons()
		elif point.startswith("buy"):
			cname = "conduit-" + point[3:]
			state.state.buy(cname)
	elif isinstance(point, parts.Conduit):
		if cursor is point:
			for j in range(len(controls)):
				if controls[j] is cursor:
					controls[j] = cursor = cursor.rotate(1)
		elif state.state.unused[point.name]:
			cursor = point
		else:
			sound.play("cantpick")
	elif isinstance(point, parts.Part):
		if cursor is point:
			cursor = None
		elif point.name in state.state.unlocked:
			if state.state.unused[point.name]:
				cursor = point
			else:
				sound.play("cantpick")
		else:
			state.state.unlock(point.name)
	elif point is None:
		cursor = None
	state.save()


def think(dt, events, mousepos):
	global mpos, cursor, point
	sound.playmusic("equip")
	if settings.pauseondialog and state.state.playing:
		dialog.think(dt)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and state.state.tline > 0.5:
				dialog.advance()
		dt = 0
	point = pointat(mousepos)
	for event in events:
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			scene.pop()
			gamescene.makebuttons()
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			handleclick()
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
			cursor = None
	mpos = mousepos
	dialog.think(dt)
	for b in buttons:
		if b.name.startswith("buy"):
			cname = "conduit-" + b.name[3:]
			b.text = "Buy: $%d\nAvail: %d" % (settings.modulecosts[cname], state.state.unused[cname])
			b.makeimg()
	for q in state.state.quests:
		q.think(dt)

def draw():
	vista.screen.fill((50, 50, 50))
	for x in range(settings.shipw):
		for y in range(settings.shiph):
			vista.screen.fill((100, 50, 0), (bx0 + bscale*x, by0 + bscale*y, bscale-3, bscale-3))
	for x0, y0, x1, y1 in state.state.supplies.values():
		dx, dy = x1 - x0, y1 - y0
		rot = {
			(1, 0): -90,
			(-1, 0): 90,
		}[(dx, dy)]
		pos = int(bx0 + (x0 + 0.5) * bscale), int(by0 + (y0 + 0.5) * bscale)
		img.draw("inflow", pos, scale = bscale / 64, angle = rot)

	for part in state.state.parts:
		on = isinstance(part, parts.Conduit) or part.name in state.state.hookup
		part.draw((bx0, by0), bscale, on = on)
	for (x0, y0, scale), control in zip(cps, controls):
		on = isinstance(control, parts.Conduit) or control.name in state.state.unlocked
		control.draw((x0, y0), scale, on = on)
		if control is cursor:
			control.drawoutline((x0, y0), scale)
	for b in buttons:
		b.draw()
	titlesize = F(34)
	subtitlesize = F(18)
	titlefont = "audiowide"
	img.drawtext("OUTFIT CAPSULE", fontsize = F(42), fontname = titlefont, color = (100, 200, 0), bottomleft = F(20, 460))
	img.drawtext("MODULES", fontsize = titlesize, fontname = titlefont, color = (200, 100, 100), midbottom = F(130, 45))
	img.drawtext("SHIP LAYOUT", fontsize = titlesize, fontname = titlefont, color = (160, 160, 160), midbottom = F(854/2, 45))
	img.drawtext("Click to remove", fontsize = subtitlesize, fontname = titlefont, color = (160, 160, 160), midtop = F(854/2, 45))
	img.drawtext("CONDUITS", fontsize = titlesize, fontname = titlefont, color = (100, 200, 100), midbottom = F(854-130, 45))
	img.drawtext("Re-click to rotate", fontsize = subtitlesize, fontname = titlefont, color = (100, 200, 100), midtop = F(854-130, 45))
	img.drawtext("Spacebucks: $%d\n " % state.state.bank, fontsize = F(24), fontname = "viga", color = (100, 0, 200), bottomright = F(840, 384))
	if isinstance(point, parts.Part) and not isinstance(point, parts.Conduit):
		info = settings.moduleinfo[point.name]
		img.drawtext(info, fontsize = F(32), fontname = "teko", midtop = F(854/2, 100), maxwidth = F(340))
		if point.name not in state.state.unlocked:
			info = "Cost to unlock: $%d" % settings.modulecosts[point.name]
			img.drawtext(info, fontsize = F(64), fontname = "teko", midtop = F(854/2, 340))
			
	if cursor is not None and mpos is not None:
		p = (mpos[0] - bx0) / bscale, (mpos[1] - by0) / bscale
		icon = cursor.nearest(p)
		bad = not state.state.canaddpart(icon)
		icon.draw((bx0, by0), bscale, bad = bad)
	dialog.draw()


