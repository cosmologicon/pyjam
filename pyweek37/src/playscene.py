import pygame, math, random
from collections import Counter
from . import control, view, grid, state, settings, hud, generate, quest, graphics, sound
from . import pview, ptext
from .pview import T



def init():
	global building
	building = None
	state.load()
	control.init()
	control.selected = None
	hud.init()

def think(dt):
	global building
	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	hud.think(dt)
	if control.click:
		if building is not None:
			if len(building.pHs) == 1 and state.planetat(pHcursor) not in [None, building.supplier]:
				building = state.Tube(pHcursor)
				sound.play("start")
			else:
				dlen = building.tryclick(pHcursor)
				if not building.supplier:
					sound.play("cancel")
					building = None
				elif building.built:
					sound.play("complete")
					state.addtube(building)
					building = None
				elif dlen > 0:
					sound.play("buildup")
				elif dlen < 0:
					sound.play("builddown")
				else:
					sound.play("no")
		else:
			control.selected = state.objat(pHcursor)
			if isinstance(control.selected, state.Planet):
				building = state.Tube(pHcursor)
				control.selected = None
				sound.play("start")
			elif isinstance(control.selected, state.Tube):
				sound.play("select")
			else:
				control.selected = None
				sound.play("click")
			
	if control.dragfrom is not None and building is None:
		dragfromH = grid.HnearestG(view.GconvertD(control.dragfrom))
		if state.planetat(dragfromH):
			building = state.Tube(dragfromH)
			sound.play("start")
			control.selected = None
	if any(control.dragD) and building is not None:
		dlen = building.trydrag(pHcursor)
		if building.built:
			sound.play("complete")
			state.addtube(building)
			building = None
		elif dlen > 0:
			sound.play("buildup")
		elif dlen < 0:
			sound.play("builddown")
		
	if building is not None and "remove" in control.kdowns:
		sound.play("cancel")
		building = None
	if control.rclick:
		building = None
		control.selected = None

	if pygame.K_TAB in control.kdowns:
		settings.expandinfo = not settings.expandinfo
		settings.save()

	if isinstance(control.selected, state.Tube):
		if "remove" in control.kdowns:
			state.removetube(control.selected)
			control.selected = None
	dx = 600 * (control.kpressed["right"] - control.kpressed["left"]) * dt
	dy = 600 * (control.kpressed["down"] - control.kpressed["up"]) * dt
	view.scootD(dx, dy)
	view.scootD(-control.mdragD[0], -control.mdragD[1])
	if control.dwheel > 0:
		view.zoomstep(1, control.posD)
	if control.dwheel < 0:
		view.zoomstep(-1, control.posD)
	for tube in state.tubes:
		tube.think(dt)
	for planet in state.planets:
		planet.think(dt)
	quest.think(dt)


def draw():
	graphics.drawground()
	pygame.draw.circle(pview.screen, (255, 200, 128), control.posD, 3)

	pHcursor = grid.HnearestG(view.GconvertD(control.posD))
	if False:
		for pH in state.visible:
			if not state.isfree(pH): continue
			pD = view.DconvertG(grid.GconvertH(pH))
			alpha = 0.4 if pH == pHcursor else 0.12
			xH, yH = pH
			ptext.draw(f"{xH},{yH}", center = pD, alpha = alpha,
				fontsize = view.DscaleG(0.6), owidth = 2)
	if building is not None:
		for nextpH in building.nexts():
			graphics.outlineH(nextpH)

	dmax = max(grid.normH(pH) for pH in state.visible)
	for pH in state.board:
		if pH not in state.visible and grid.normH(pH) < dmax + 2:
#			graphics.drawcircleH(pH, (255, 255, 255), 0.4)
			graphics.drawcloudatH(pH)
	graphics.fog(dmax)

	for rock in state.rocks:
		rock.draw()
	for tube in state.tubes:
		tube.draw()
	for planet in state.planets:
		planet.draw()
	graphics.renderqueue()

	if building is not None:
		building.drawglow()
	if control.selected is not None:
		control.selected.drawglow()

	for tube in state.tubes:
		tube.drawcarry()
	graphics.renderqueue()
	for planet in state.planets:
		planet.drawbubbles()
	graphics.renderqueue()


	graphics.drawsand()

	hud.draw()

	marquee = quest.marquee()
	if marquee:
		ptext.draw(marquee, width = T(800), midbottom = T(640, 690),
			fontsize = T(40), shade = 1, owidth = 1)

	if settings.expandinfo:
		lines = [
			"Left click or drag: build conduit",
			"Right drag or WASD: pan",
			"Scroll wheel or 1/2: zoom",
			"Backspace: delete conduit",
			"Tab: hide controls",
		]
	else:
		lines = ["Tab: expand controls"]
	if control.selected is not None:
		lines = control.selected.info() + lines
	ptext.draw("\n".join(lines), bottomright = pview.bottomright, fontsize = T(25),
		owidth = 1)



